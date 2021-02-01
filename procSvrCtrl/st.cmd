#!/epics/modules/procServControl/bin/linux-x86_64/procServControl

< envPaths
< /epics/common/xf28id2-ioc1-netsetup.cmd

dbLoadDatabase("$(PROCSERVCONTROL)/dbd/procServControl.dbd",0,0)
procServControl_registerRecordDeviceDriver(pdbbase)

drvAsynIPPortConfigure("port1",  "localhost:4058",  100, 0, 0)
drvAsynIPPortConfigure("port2",  "localhost:4069",  100, 0, 0)
drvAsynIPPortConfigure("port3",  "localhost:4070",  100, 0, 0)
drvAsynIPPortConfigure("port4",  "localhost:4065",  100, 0, 0)
drvAsynIPPortConfigure("port5",  "localhost:4071",  100, 0, 0)
drvAsynIPPortConfigure("port6",  "localhost:4057",  100, 0, 0)
drvAsynIPPortConfigure("port7",  "localhost:6002",  100, 0, 0)
drvAsynIPPortConfigure("port8",  "localhost:6666",  100, 0, 0)
drvAsynIPPortConfigure("port9",  "localhost:4050",  100, 0, 0)
drvAsynIPPortConfigure("port10",  "localhost:4051",  100, 0, 0)
drvAsynIPPortConfigure("port11",  "localhost:4052",  100, 0, 0)
drvAsynIPPortConfigure("port12",  "localhost:4053",  100, 0, 0)
drvAsynIPPortConfigure("port13",  "localhost:4054",  100, 0, 0)
drvAsynIPPortConfigure("port14",  "localhost:4061",  100, 0, 0)
drvAsynIPPortConfigure("port15",  "localhost:4067",  100, 0, 0)
drvAsynIPPortConfigure("port16",  "localhost:4062",  100, 0, 0)
drvAsynIPPortConfigure("port17",  "localhost:4075",  100, 0, 0)
drvAsynIPPortConfigure("port18",  "localhost:4083",  100, 0, 0)
drvAsynIPPortConfigure("port19",  "localhost:4080",  100, 0, 0)
drvAsynIPPortConfigure("port20",  "localhost:4081",  100, 0, 0)
drvAsynIPPortConfigure("port21",  "localhost:5050",  100, 0, 0)
drvAsynIPPortConfigure("port22",  "localhost:5051",  100, 0, 0)
drvAsynIPPortConfigure("port23",  "localhost:5052",  100, 0, 0)
drvAsynIPPortConfigure("port24",  "localhost:5053",  100, 0, 0)
drvAsynIPPortConfigure("port25",  "localhost:5054",  100, 0, 0)
drvAsynIPPortConfigure("port26",  "localhost:5055",  100, 0, 0)
drvAsynIPPortConfigure("port27",  "localhost:5070",  100, 0, 0)
drvAsynIPPortConfigure("port28",  "localhost:5001",  100, 0, 0)
drvAsynIPPortConfigure("port29",  "localhost:4040",  100, 0, 0)
drvAsynIPPortConfigure("port30",  "localhost:4090",  100, 0, 0)
drvAsynIPPortConfigure("port31",  "localhost:4060",  100, 0, 0)
drvAsynIPPortConfigure("port32",  "localhost:4068",  100, 0, 0)
drvAsynIPPortConfigure("port33",  "localhost:4066",  100, 0, 0)
drvAsynIPPortConfigure("port34",  "localhost:4077",  100, 0, 0)
drvAsynIPPortConfigure("port35",  "localhost:4056",  100, 0, 0)
drvAsynIPPortConfigure("port36",  "localhost:4106",  100, 0, 0)
drvAsynIPPortConfigure("port37",  "localhost:4072",  100, 0, 0)

dbLoadTemplate("procServControl.substitutions")

iocInit()

dbl > records.dbl

seq(procServControl,"P=XF:28IDC-CT{{IOC:Cam04}")
seq(procServControl,"P=XF:28IDC-CT{{IOC:Cam07}")
seq(procServControl,"P=XF:28IDC-CT{{IOC:Env01}")
seq(procServControl,"P=XF:28IDC-CT{{IOC:Env02}")
seq(procServControl,"P=XF:28IDC-CT{{IOC:Env03}")
seq(procServControl,"P=XF:28IDC-CT{{IOC:IM01}")
seq(procServControl,"P=XF:28IDC-CT{{IOC:LINKAM}")
seq(procServControl,"P=XF:28ID2-CT{{IOC:MANA}")
seq(procServControl,"P=XF:28IDC-CT{{IOC:MC01}")
seq(procServControl,"P=XF:28IDC-CT{{IOC:MC02}")
seq(procServControl,"P=XF:28IDC-CT{{IOC:MC03}")
seq(procServControl,"P=XF:28IDC-CT{{IOC:MC04}")
seq(procServControl,"P=XF:28IDC-CT{{IOC:MC05}")
seq(procServControl,"P=XF:28IDC-CT{{IOC:MC06}")
seq(procServControl,"P=XF:28IDC-CT{{IOC:MC07}")
seq(procServControl,"P=XF:28IDC-CT{{IOC:MC08}")
seq(procServControl,"P=XF:28IDC-OP:1{{IOC:MC09}")
seq(procServControl,"P=XF:28IDC-CT{{IOC:MC10}")
seq(procServControl,"P=XF:28IDC-CT{{IOC:MC12}")
seq(procServControl,"P=XF:28IDC-CT{{IOC:MC13}")
seq(procServControl,"P=XF:28IDD-CT{{IOC:MC14}")
seq(procServControl,"P=XF:28IDD-CT{{IOC:MC15}")
seq(procServControl,"P=XF:28IDD-CT{{IOC:MC16}")
seq(procServControl,"P=XF:28IDD-CT{{IOC:MC17}")
seq(procServControl,"P=XF:28IDD-CT{{IOC:MC18}")
seq(procServControl,"P=XF:28IDD-CT{{IOC:MC19}")
seq(procServControl,"P=XF:28IDD-CT{{IOC:PIC884}")
seq(procServControl,"P=XF:28IDD-CT{{IOC:PID}")
seq(procServControl,"P=XF:28ID-CT{{IOC:EPS}")
seq(procServControl,"P=XF:28IDC-CT{{IOC:PUMP1}")
seq(procServControl,"P=XF:28IDC-CT{{IOC:IM02}")
seq(procServControl,"P=XF:28IDC-CT{{IOC:RGA1}")
seq(procServControl,"P=XF:28IDC-CT{{IOC:SM1}")
seq(procServControl,"P=XF:28IDC-CT{{IOC:STATS1}")
seq(procServControl,"P=XF:28IDC-CT{{IOC:VA01}")
seq(procServControl,"P=XF:DetLab{{IOC:VA}")
seq(procServControl,"P=XF:28IDC-CT{{IOC:VMEMon1}")
dbpf XF:28IDC-CT{{IOC:Cam04}SHOWOUT 0
dbpf XF:28IDC-CT{{IOC:Cam07}SHOWOUT 0
dbpf XF:28IDC-CT{{IOC:Env01}SHOWOUT 0
dbpf XF:28IDC-CT{{IOC:Env02}SHOWOUT 0
dbpf XF:28IDC-CT{{IOC:Env03}SHOWOUT 0
dbpf XF:28IDC-CT{{IOC:IM01}SHOWOUT 0
dbpf XF:28IDC-CT{{IOC:LINKAM}SHOWOUT 0
dbpf XF:28ID2-CT{{IOC:MANA}SHOWOUT 0
dbpf XF:28IDC-CT{{IOC:MC01}SHOWOUT 0
dbpf XF:28IDC-CT{{IOC:MC02}SHOWOUT 0
dbpf XF:28IDC-CT{{IOC:MC03}SHOWOUT 0
dbpf XF:28IDC-CT{{IOC:MC04}SHOWOUT 0
dbpf XF:28IDC-CT{{IOC:MC05}SHOWOUT 0
dbpf XF:28IDC-CT{{IOC:MC06}SHOWOUT 0
dbpf XF:28IDC-CT{{IOC:MC07}SHOWOUT 0
dbpf XF:28IDC-CT{{IOC:MC08}SHOWOUT 0
dbpf XF:28IDC-OP:1{{IOC:MC09}SHOWOUT 0
dbpf XF:28IDC-CT{{IOC:MC10}SHOWOUT 0
dbpf XF:28IDC-CT{{IOC:MC12}SHOWOUT 0
dbpf XF:28IDC-CT{{IOC:MC13}SHOWOUT 0
dbpf XF:28IDD-CT{{IOC:MC14}SHOWOUT 0
dbpf XF:28IDD-CT{{IOC:MC15}SHOWOUT 0
dbpf XF:28IDD-CT{{IOC:MC16}SHOWOUT 0
dbpf XF:28IDD-CT{{IOC:MC17}SHOWOUT 0
dbpf XF:28IDD-CT{{IOC:MC18}SHOWOUT 0
dbpf XF:28IDD-CT{{IOC:MC19}SHOWOUT 0
dbpf XF:28IDD-CT{{IOC:PIC884}SHOWOUT 0
dbpf XF:28IDD-CT{{IOC:PID}SHOWOUT 0
dbpf XF:28ID-CT{{IOC:EPS}SHOWOUT 0
dbpf XF:28IDC-CT{{IOC:PUMP1}SHOWOUT 0
dbpf XF:28IDC-CT{{IOC:IM02}SHOWOUT 0
dbpf XF:28IDC-CT{{IOC:RGA1}SHOWOUT 0
dbpf XF:28IDC-CT{{IOC:SM1}SHOWOUT 0
dbpf XF:28IDC-CT{{IOC:STATS1}SHOWOUT 0
dbpf XF:28IDC-CT{{IOC:VA01}SHOWOUT 0
dbpf XF:DetLab{{IOC:VA}SHOWOUT 0
dbpf XF:28IDC-CT{{IOC:VMEMon1}SHOWOUT 0
