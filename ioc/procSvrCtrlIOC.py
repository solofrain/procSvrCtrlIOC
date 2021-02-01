#!/usr/bin/python3
#=================================
# Author: Ji Li <liji@bn.gov>
#=================================
import os

STATUS_LIST_FILE = "status.list"
REPORT_LIST_FILE = "report.list"

SUB_FILE = "procSvrCtrl/procServControl.substitutions"
ST_CMD_FILE = "procSvrCtrl/st.cmd"
#ENV_PATHS_FILE = "procSvrCtrl/envPaths"
CONFIG_FILE = "procSvrCtrl/config"

status_list = []
ioc_list = []
ignore_list = ["procSvrCtrl", "test", "test1", "test2", "omega_i_series"]
no_rec_list = []
no_pv_list = []
hostname =[]

#==========================================
# Get the index of n-th appearance
#==========================================
def nth_index(string, substring, num):
    if num==1:
        if substring in string:
            return string.index(substring)
        else:
            return -1
    else:
        ind = string.index(substring)
        leng = len(substring)
        sub_ind = nth_index(string[ind+leng:len(string)], substring, num-1)
        if sub_ind<0:
            return -1
        else:
            return ind + leng + sub_ind
#==========================================

#==========================================
# Get a list of active IOCs
#==========================================
def get_iocs():
    global status_list
    global ioc_list
    global no_rec_list
    global no_pv_list

    # Get active IOCs
    with open (STATUS_LIST_FILE, 'r') as f:
        for line in f:
            if '/etc/init.d' not in line:
                #print(line + " is an invalid record")
                continue

            status_profile = line.split('\t')
            ioc = status_profile[0][20:len(status_profile[0])]
            if ioc in ignore_list:
                print(ioc + " ignored.")
                continue
                
            status = status_profile[len(status_profile)-1]
            if "Stopped" in status and "Not registered" in status:
                print(ioc + " is inactive.")
                continue

            status_list.append(ioc)

    f.close()


    # Get directories of the IOCs
    with open (REPORT_LIST_FILE, 'r') as f:
        for line in f:
            if '/epics/iocs' not in line:
                #print(line + " is an invalid record")
                continue

            report = line.split('|')
            ioc= report[1].strip()
            
            if ioc not in status_list:
                continue

            if "/epics/iocs" not in report[4]: 
                print(ioc + " is not a regular ioc.")
                continue

            index = report[4].index('/')
            folder = report[4][index:index+12]
            report[4] = report[4][index+12:len(report[4])]
            index = report[4].index('/')
            folder = folder + report[4][0:index]

            port = report[3].strip()
            ioc_list.append({'ioc':ioc,
                             'port': port,
                             'dir': folder})

    f.close()

#==========================================


#==========================================
# Get names of the IOCs from PVs
# Need records.dbl in the IOC directory.
#==========================================
def get_iocnames():
    for i in range(len(ioc_list)-1, -1, -1):
        record_file = ioc_list[i]['dir'] + "/records.dbl"

        if os.path.exists(record_file):
            process = os.popen("grep -m 1 IOC: " + record_file)
            pv = process.read()
            process.close()

            if "XF" not in pv:
                print("Information not found in " + pv)
                no_pv_list.append(ioc_list[i]['dir'])
                ioc_list.pop(i)
                continue
            pv = pv.replace("\n", "")
            
            sys = pv[0:pv.index('{')]
            iocname = pv[pv.index('{')+1:pv.index('}')]
            ioc_list[i]['sys'] = sys
            ioc_list[i]['iocname'] = iocname
        else:
            print("No records.dbl in " + ioc_list[i]['dir'])
            no_rec_list.append(ioc_list[i]['dir'])
            ioc_list.pop(i)
            
#==========================================



#==========================================
# Create .substitutions file
#==========================================
def create_sub_file():
    print("Creating .substitutions file...")
    global ioc_list

    f = open(SUB_FILE, 'w')
    
    f.write("global {\n")
    f.write('    SHOWOUT = "1"\n')
    f.write('    manualstart = ""\n')
    f.write("}\n")
    f.write("\n")
    f.write('file "db/procServControl.db"\n')
    f.write("{\n")
    f.write("pattern\n")
    f.write("{ SYS , DEV , PORT }\n")

    for i in range(len(ioc_list)):
        f.write("{ ")
        f.write(ioc_list[i]['sys'])
        f.write(" , ")
        f.write(ioc_list[i]['iocname'])
        f.write(" , port")
        f.write(str(i+1))
        f.write(" }\n")

    f.write("}\n")
            
    f.close()

#==========================================


#==========================================
# Create st.cmd
#==========================================
def create_st_cmd():
    print("Creating st.cmd...")
    global ioc_list
    global hostname

    process = os.popen("hostname")
    hostname = process.read()
    hostname = hostname.replace("\n", "")
    process.close()

    f = open(ST_CMD_FILE, 'w')

    f.write("#!../../bin/linux-x86_64/procServControl\n\n")
    f.write('< envPaths\n')
    f.write('< /epics/common/' + hostname + '-netsetup.cmd\n\n')

    f.write('cd $(TOP)\n')

    f.write('dbLoadDatabase("dbd/procServControl.dbd",0,0)\n')
    f.write('procServControl_registerRecordDeviceDriver(pdbbase)\n\n')


    for i in range(len(ioc_list)):
        f.write('drvAsynIPPortConfigure("port' + str(i+1) + '",  "localhost:' + ioc_list[i]['port'] + '",  100, 0, 0)\n')

    f.write('\ndbLoadTemplate("db/procServControl.substitutions")\n\n')

    f.write('iocInit()\n\n')

    f.write('dbl > records.dbl\n\n')

    for i in range(len(ioc_list)):
        f.write('seq(procServControl,"P=' + ioc_list[i]['sys'] + '{' + ioc_list[i]['iocname'] + '}")\n')

    for i in range(len(ioc_list)):
        f.write('dbpf ' + ioc_list[i]['sys'] + '{' + ioc_list[i]['iocname'] + '}SHOWOUT 0\n')

    f.close()
#==========================================

#==========================================
# Create envPaths
#==========================================
#def create_env_paths():
#    print('Creating envPaths...')
#
#    f = open(ENV_PATHS_FILE, 'w')
#
#    f.write('epicsEnvSet("PROCSERVCONTROL", "/epics/modules/procServControl")\n')
#
#    f.close()
#==========================================


#==========================================
# Create config
#==========================================
def create_config():
    print('Creating config...')

    global hostname
    process = os.popen("manage-iocs nextport")
    port = process.read()
    process.close()

    f = open(CONFIG_FILE, 'w')

    f.write('NAME=procServControl\n')
    f.write('USER=softioc\n')
    f.write('PORT=' + port)
    f.write('HOST=' + hostname)

    f.close()
#==========================================

def create_opi():
    print("Creating .opi file...")

    global hostname

    bl = hostname[2:4] + hostname[4:6].upper()
    HOSTNAME = hostname.upper()
    BL = HOSTNAME[2:6]

    num_iocs = len(ioc_list)
    group_container_height = 60 + num_iocs*26
    link_container_x = 20
    link_container_y = 20
    link_container_height = 26
    link_container_width = 905
    link_opi_file = '../../common/ct/ioc_single_line_ext.opi'

    f = open(hostname+".opi", 'w')

    # 
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<display typeId="org.csstudio.opibuilder.Display" version="1.0.0">\n')
    f.write('  <actions hook="false" hook_all="false" />\n')
    f.write('  <auto_scale_widgets>\n')
    f.write('    <auto_scale_widgets>false</auto_scale_widgets>\n')
    f.write('    <min_width>-1</min_width>\n')
    f.write('    <min_height>-1</min_height>\n')
    f.write('  </auto_scale_widgets>\n')
    f.write('  <auto_zoom_to_fit_all>false</auto_zoom_to_fit_all>\n')
    f.write('  <background_color>\n')
    f.write('    <color red="240" green="240" blue="240" />\n')
    f.write('  </background_color>\n')
    f.write('  <boy_version>5.1.0.201706291447</boy_version>\n')
    f.write('  <foreground_color>\n')
    f.write('    <color red="192" green="192" blue="192" />\n')
    f.write('  </foreground_color>\n')
    f.write('  <grid_space>6</grid_space>\n')
    f.write('  <height>1500</height>\n')
    f.write('  <macros>\n')
    f.write('    <include_parent_macros>true</include_parent_macros>\n')
    f.write('    <TITLE>' + BL + ' IOCs</TITLE>\n')
    f.write('  </macros>\n')
    f.write('  <name></name>\n')
    f.write('  <rules />\n')
    f.write('  <scripts />\n')
    f.write('  <show_close_button>true</show_close_button>\n')
    f.write('  <show_edit_range>true</show_edit_range>\n')
    f.write('  <show_grid>true</show_grid>\n')
    f.write('  <show_ruler>true</show_ruler>\n')
    f.write('  <snap_to_geometry>true</snap_to_geometry>\n')
    f.write('  <widget_type>Display</widget_type>\n')
    f.write('  <width>1080</width>\n')
    f.write('  <wuid>-77f41667:14a6d5da675:-72ab</wuid>\n')
    f.write('  <x>0</x>\n')
    f.write('  <y>0</y>\n')
    f.write('  <widget typeId="org.csstudio.opibuilder.widgets.linkingContainer" version="1.0.0">\n')
    f.write('    <actions hook="false" hook_all="false" />\n')
    f.write('    <background_color>\n')
    f.write('      <color red="240" green="240" blue="240" />\n')
    f.write('    </background_color>\n')
    f.write('    <border_color>\n')
    f.write('      <color red="0" green="128" blue="255" />\n')
    f.write('    </border_color>\n')
    f.write('    <border_style>0</border_style>\n')
    f.write('    <border_width>1</border_width>\n')
    f.write('    <enabled>true</enabled>\n')
    f.write('    <font>\n')
    f.write('      <opifont.name fontName="Sans" height="10" style="0" pixels="false">Default</opifont.name>\n')
    f.write('    </font>\n')
    f.write('    <foreground_color>\n')
    f.write('      <color red="192" green="192" blue="192" />\n')
    f.write('    </foreground_color>\n')
    f.write('    <group_name></group_name>\n')
    f.write('    <height>51</height>\n')
    f.write('    <macros>\n')
    f.write('      <include_parent_macros>true</include_parent_macros>\n')
    f.write('    </macros>\n')
    f.write('    <name>Linking Container_24</name>\n')
    f.write('    <opi_file>../../common/title_1080.opi</opi_file>\n')
    f.write('    <resize_behaviour>1</resize_behaviour>\n')
    f.write('    <rules />\n')
    f.write('    <scale_options>\n')
    f.write('      <width_scalable>true</width_scalable>\n')
    f.write('      <height_scalable>true</height_scalable>\n')
    f.write('      <keep_wh_ratio>false</keep_wh_ratio>\n')
    f.write('    </scale_options>\n')
    f.write('    <scripts />\n')
    f.write('    <tooltip></tooltip>\n')
    f.write('    <visible>true</visible>\n')
    f.write('    <widget_type>Linking Container</widget_type>\n')
    f.write('    <width>950</width>\n')
    f.write('    <wuid>-77f41667:14a6d5da675:-7212</wuid>\n')
    f.write('    <x>0</x>\n')
    f.write('    <y>0</y>\n')
    f.write('  </widget>\n')

    f.write('  <widget typeId="org.csstudio.opibuilder.widgets.groupingContainer" version="1.0.0">\n')
    f.write('    <actions hook="false" hook_all="false" />\n')
    f.write('    <background_color>\n')
    f.write('      <color red="240" green="240" blue="240" />\n')
    f.write('    </background_color>\n')
    f.write('    <border_color>\n')
    f.write('      <color name="NSLS2Blue" red="3" green="116" blue="176" />\n')
    f.write('    </border_color>\n')
    f.write('    <border_style>12</border_style>\n')
    f.write('    <border_width>1</border_width>\n')
    f.write('    <enabled>true</enabled>\n')
    f.write('    <fc>false</fc>\n')
    f.write('    <font>\n')
    f.write('      <opifont.name fontName="Sans" height="10" style="0" pixels="false">Default</opifont.name>\n')
    f.write('    </font>\n')
    f.write('    <foreground_color>\n')
    f.write('      <color red="192" green="192" blue="192" />\n')
    f.write('    </foreground_color>\n')
    f.write('    <height>' + str(group_container_height) + '</height>\n')
    f.write('    <lock_children>false</lock_children>\n')
    f.write('    <macros>\n')
    f.write('      <include_parent_macros>true</include_parent_macros>\n')
    f.write('    </macros>\n')
    f.write('    <name>' + HOSTNAME + ' IOCs</name>\n')
    f.write('    <rules />\n')
    f.write('    <scale_options>\n')
    f.write('      <width_scalable>true</width_scalable>\n')
    f.write('      <height_scalable>true</height_scalable>\n')
    f.write('      <keep_wh_ratio>false</keep_wh_ratio>\n')
    f.write('    </scale_options>\n')
    f.write('    <scripts />\n')
    f.write('    <show_scrollbar>true</show_scrollbar>\n')
    f.write('    <tooltip></tooltip>\n')
    f.write('    <transparent>false</transparent>\n')
    f.write('    <visible>true</visible>\n')
    f.write('    <widget_type>Grouping Container</widget_type>\n')
    f.write('    <width>960</width>\n')
    f.write('    <wuid>-77f41667:14a6d5da675:-71ef</wuid>\n')
    f.write('    <x>35</x>\n')
    f.write('    <y>80</y>\n')

    for i in range(num_iocs):
        f.write('    <widget typeId="org.csstudio.opibuilder.widgets.linkingContainer" version="1.0.0">\n')
        f.write('      <actions hook="false" hook_all="false" />\n')
        f.write('      <background_color>\n')
        f.write('        <color red="240" green="240" blue="240" />\n')
        f.write('      </background_color>\n')
        f.write('      <border_color>\n')
        f.write('        <color red="0" green="128" blue="255" />\n')
        f.write('      </border_color>\n')
        f.write('      <border_style>15</border_style>\n')
        f.write('      <border_width>1</border_width>\n')
        f.write('      <enabled>true</enabled>\n')
        f.write('      <font>\n')
        f.write('        <opifont.name fontName="Sans" height="10" style="0" pixels="false">Default</opifont.name>\n')
        f.write('      </font>\n')
        f.write('      <foreground_color>\n')
        f.write('        <color red="192" green="192" blue="192" />\n')
        f.write('      </foreground_color>\n')
        f.write('      <group_name></group_name>\n')
        f.write('      <height>' + str(link_container_height) + '</height>\n')
        f.write('      <macros>\n')
        f.write('        <include_parent_macros>true</include_parent_macros>\n')
        f.write('        <ioc>' + ioc_list[i]['sys'] + '{' + ioc_list[i]['iocname'] + '}</ioc>\n')
        f.write('      </macros>\n')
        f.write('      <name>Linking Container_1</name>\n')
        f.write('      <opi_file>' + link_opi_file + '</opi_file>\n')
        f.write('      <resize_behaviour>1</resize_behaviour>\n')
        f.write('      <rules />\n')
        f.write('      <scale_options>\n')
        f.write('        <width_scalable>true</width_scalable>\n')
        f.write('        <height_scalable>true</height_scalable>\n')
        f.write('        <keep_wh_ratio>false</keep_wh_ratio>\n')
        f.write('      </scale_options>\n')
        f.write('      <scripts />\n')
        f.write('      <tooltip></tooltip>\n')
        f.write('      <visible>true</visible>\n')
        f.write('      <widget_type>Linking Container</widget_type>\n')
        f.write('      <width>' + str(link_container_height) + '</width>\n')
        f.write('      <wuid>-5b22a43f:14d05e807b0:-7d33</wuid>\n')
        f.write('      <x>' + str(link_container_x) + '</x>\n')
        f.write('      <y>' + str(link_container_y) + '</y>\n')
        f.write('    </widget>\n')
        link_container_y = link_container_y + link_container_height

    f.write('  </widget>\n')
    f.write('</display>\n')

    f.close()

os.system("manage-iocs status > " + STATUS_LIST_FILE)
os.system("manage-iocs report > " + REPORT_LIST_FILE)

get_iocs()

get_iocnames()

if os.path.exists("procSvrCtrl"):
    os.system("rm -r procSvrCtrl")
os.system('mkdir procSvrCtrl')

create_sub_file()

create_st_cmd()

#create_env_paths()

create_config()

create_opi()

os.system("rm status.list")
os.system("rm report.list")

print("==========================================================")

print("Info: " + str(len(ioc_list)) + " IOCs found")

print("==========================================================")

if len(no_rec_list)>0:
    print("WARNING: The following IOCs don't have records.dbl")
    for i in range(len(no_rec_list)):
        print(no_rec_list[i])

    print("==========================================================")

if len(no_pv_list)>0:
    print("WARNING: The following IOCs don't have IOC name in PV")
    for i in range(len(no_pv_list)):
        print(no_pv_list[i])

    print("==========================================================")
