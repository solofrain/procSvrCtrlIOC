TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = procServControl
# procServControl.dbd will be created and installed
DBD += procServControl.dbd

# procServControl.dbd will be made up from these files:
procServControl_DBD += base.dbd
procServControl_DBD += asyn.dbd
procServControl_DBD += drvAsynIPPort.dbd
procServControl_DBD += busySupport.dbd
procServControl_DBD += proc.dbd

# Include dbd files from all support applications:
#procServControl_DBD += xxx.dbd

# Add all the support libraries needed by this IOC
#procServControl_LIBS += xxx

# procServControl_registerRecordDeviceDriver.cpp derives from procServControl.dbd
procServControl_SRCS += procServControl_registerRecordDeviceDriver.cpp
procServControl_SRCS += procServControl.st

# Build the main IOC entry point on workstation OSs.
procServControl_SRCS_DEFAULT += procServControlMain.cpp
procServControl_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#procServControl_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
procServControl_LIBS += $(EPICS_BASE_IOC_LIBS)
procServControl_LIBS += busy
procServControl_LIBS += seq
procServControl_LIBS += pv
procServControl_LIBS += asyn

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

