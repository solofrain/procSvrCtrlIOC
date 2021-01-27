#!/usr/bin/python3
#=================================
# Author: Ji Li <liji@bn.gov
#=================================
from parse import parse
import os

STATUS_LIST_FILE = "status.list"
REPORT_LIST_FILE = "report.list"

SUB_FILE = "procSvrCtrl/procServControl.substitutions"
ST_CMD_FILE = "procSvrCtrl/st.cmd"
ENV_PATHS_FILE = "procSvrCtrl/envPaths"
CONFIG_FILE = "procSvrCtrl/config"

status_list = []
ioc_list = []
ignore_list = ["procSvrCtrl"]
no_rec_list = []
no_pv_list = []
hostname =[]

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
            status_profile = parse("/etc/init.d/softioc-{ioc}\t\t{status}", line)
            
            if status_profile['ioc'] in ignore_list:
                print(status_profile['ioc'] + " ignored.")
                continue

            if ("Not" in status_profile['status']):
                print(status_profile['ioc'] + " is inactive.")
                continue

            if (status_profile!= None):
                status_list.append(status_profile['ioc'])

    # Get directories of the IOCs
    with open (REPORT_LIST_FILE, 'r') as f:
        for line in f:
            line = line.replace(" ", "")
            report_profile = parse("/epics/iocs|{ioc}|{user}|{port}|{stcmd}", line)
            if (report_profile == None):
                continue

            if report_profile['ioc'] in status_list:
                if "/epics/iocs/" in report_profile['stcmd']:
                    profile = parse("/epics/iocs/{folder}/{dontcare}",
                                    report_profile['stcmd'])

                    ioc_list.append({'ioc':report_profile['ioc'],
                                     'port': report_profile['port'],
                                     'dir': profile['folder']})
                else:
                    print(report_profile['ioc'] + " is not a regular ioc.")
            else:
                print(report_profile['ioc'] + " is inactive.")

#==========================================


#==========================================
# Get names of the IOCs from PVs
# Need records.dbl in the IOC directory.
#==========================================
def get_iocnames():
    for i in range(len(ioc_list)-1, -1, -1):
        record_file = "/epics/iocs/" + ioc_list[i]['dir'] + "/records.dbl"

        if os.path.exists(record_file):
            process = os.popen("grep -m 1 IOC: " + record_file)
            pv = process.read()
            pv = pv.replace("\n", "")
            process.close()

            pv_profile = parse("{sys}{{{iocname}}}{dontcare}",pv)
            if (pv_profile==None):
                print("Information not found in " + pv)
                no_pv_list.append("/epics_iocs/" + ioc_list[i]['dir'])
                ioc_list.pop(i)
                continue
            ioc_list[i]['sys'] = pv_profile['sys']
            ioc_list[i]['iocname'] = pv_profile['iocname']
        else:
            print("No records.dbl in /epics/iocs/" + ioc_list[i]['dir'])
            no_rec_list.append("/epics_iocs/" + ioc_list[i]['dir'])
            ioc_list.pop(i)
#==========================================



#==========================================
# Create .substitutions file
#==========================================
def create_sub_file():
    global ioc_list

    f = open(SUB_FILE, 'w')
    
    f.write("global {\n")
    f.write('    SHOWOUT = "1"\n')
    f.write('    manualstart = ""\n')
    f.write("}\n")
    f.write("\n")
    f.write('file "$(PROCSERVCONTROL)/db/procServControl.db"\n')
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
    global ioc_list
    global hostname

    process = os.popen("hostname")
    hostname = process.read()
    hostname = hostname.replace("\n", "")
    process.close()

    f = open(ST_CMD_FILE, 'w')

    f.write("#!/epics/modules/procServControl/bin/linux-x86_64/procServControl\n\n")
    f.write('< envPaths\n')
    f.write('< /epics/common/' + hostname + '-netsetup.cmd\n\n')

    f.write('dbLoadDatabase("$(PROCSERVCONTROL)/dbd/procServControl.dbd",0,0)\n')
    f.write('procServControl_registerRecordDeviceDriver(pdbbase)\n\n')


    for i in range(len(ioc_list)):
        f.write('drvAsynIPPortConfigure("port' + str(i+1) + '",  "localhost:' + ioc_list[i]['port'] + '",  100, 0, 0)\n')

    f.write('\ndbLoadTemplate("procServControl.substitutions")\n\n')

    f.write('iocInit()\n\n')

    f.write('dbl > records.dbl\n\n')

    for i in range(len(ioc_list)):
        f.write('seq(procServControl,"P=' + ioc_list[i]['sys'] + '{' + ioc_list[i]['iocname'] + '}")\n')


    f.close()
#==========================================

#==========================================
# Create envPaths
#==========================================
def create_env_paths():
    f = open(ENV_PATHS_FILE, 'w')

    f.write('epicsEnvSet("PROCSERVCONTROL", "/epics/modules/procServControl")\n')

    f.close()
#==========================================


#==========================================
# Create config
#==========================================
def create_config():
    global hostname

    f = open(CONFIG_FILE, 'w')

    f.write('NAME=procSvrCtrl\n')
    f.write('USER=softioc')
    f.write('PORT=9999')
    f.write('HOST=' + hostname)

    f.close()
#==========================================



os.system("manage-iocs status > " + STATUS_LIST_FILE)
os.system("manage-iocs report > " + REPORT_LIST_FILE)

get_iocs()

get_iocnames()

os.system('mkdir procSvrCtrl')

create_sub_file()

create_st_cmd()

create_env_paths()

create_config()

os.system("rm status.list")
os.system("rm report.list")

print("==========================================================")

print("Info: " + str(len(ioc_list)) + " IOCs found")

print("==========================================================")

print("WARNING: The following IOCs don't have records.dbl")
for i in range(len(no_rec_list)):
    print(no_rec_list[i])

print("==========================================================")

print("WARNING: The following IOCs don't have IOC name in PV")
for i in range(len(no_pv_list)):
    print(no_pv_list[i])

print("==========================================================")
