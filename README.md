This Python script creates an IOC for procServControl which is available at:

http://controls.diamond.ac.uk/downloads/support/procServControl/

## Usage

- Create an IOC procServControl using the files in procServControl/.
- Run ioc/procSvrCtrlIOC.py to generate host dependent files in ioc/procSvrCtrl/.
- Copy these files to`the created IOC directory.
- Build, install and start the IOC.
- Refer to the created ioc/.opi for the screen. You may need to combine several such files for one beamline.

## Note

- The script obtains IOC status and directories using manage-iocs.
- It fetches IOC names from`PVs containing such information (e.g., XF:28IDA-CT{IOC:MC1}xxx) in records.dbl files in IOC directories.
- Since the procServer can only be connected locally, one instance of the IOC is needed on each IOC server.
- You can ignore IOCs in ignore_list[].
- T
