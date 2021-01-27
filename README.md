This Python script creates an IOC for procServControl which is available at:

http://controls.diamond.ac.uk/downloads/support/procServControl/

## Note

- procServControl module should be pre-built in `/epics/modules/`;
- It obtains IOC status and directories using manage-iocs;
- It fetches IOC names from `records.dbl` files in IOC directories;
- It assumes PVs that contains IOC names (`$(Sys){IOC:$(iocname)}xxx`) exist in `records.dbl`.

## Python module used

- parse (https://pypi.org/project/parse/)

## Usage

- Run the script;
- Copy the created folder to `/epics/iocs/`;
- Install and start.
