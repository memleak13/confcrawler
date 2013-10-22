#!/usr/bin/python
"""
    Name:     confcrawler
    Version:  0.1 
    Author:   Antares
    Modified: 22.10.13
    
    !!! BEFORE THIS SCRIPT IS RUN ONE NEEDS TO CREATE THE XML CONFIG FILE
    (./cc_create_conf.py) !!!

    This script is run by a cron job. It retrieves configurations from cisco
    devices by connecting to them over telnet. These devices are stored in a 
    seperate file called ./devicelist. It has the possibility to execute
    different commands which are stored in a file called ./commandlist.
    The configs are stored in the directory ./device_configs by appending the
    date to the name of the device.

    Files:  ./cc_create_conf        creates inital layout of xml storage file
            ./web/device_configs/:  stores pulled configurations
            ./conf/commandlist:     contains commands (1 each line)
            ./conf/devicelist:      stores devices (hostname ip)
            ./conf/conf.xml:        stores devices (hostname ip)
            ./cc_globals:           contains global variables   
            ./cc_device:            device class 
            ./j_connect:            connect module (telnet)        

    Install cronjob :   
        1. crontab -e
        2. 55 23 * * * /home/tbsadmin/projects/confcrawler/confcrawler.py 
            > /home/tbsadmin/cronlog 2>&1
 
    #Todo: 
        1. Error Handling if xml file does not exist !!!
        2. Move cc_create_conf code to cc_dbaccess.py
"""
import os
from cc_device import Device
from cc_globals import Globals
from cc_dbaccess import XMLConfig

class ConfCrawler(object):
    """ Main class

    Reads device and command list. For each device a new thread is created.
    """
    def __init__(self):
        
        #Credentials
        uid = 'xxx'
        pw = 'xxx'

        #Setting global variables and paths (stored in cc_globals)
        rootdir = os.path.dirname(__file__)
        Globals.dir_rootdir = rootdir
        Globals.dir_deviceconfig = os.path.join(rootdir, 'web/device_configs/')
        Globals.file_devicelist = os.path.join(rootdir, 'conf/devicelist')
        Globals.file_commandlist = os.path.join(rootdir, 'conf/commandlist')
        Globals.file_configuration = os.path.join(rootdir, 'conf/conf.xml')

        #Global = Globals()
        #Global.print_globals()
        
        fh_device_list = open (Globals.file_devicelist, 'r')
        fh_command_list = open (Globals.file_commandlist, 'r')
        db_config = XMLConfig()

        #read command list
        commandlist = [line for line in fh_command_list]
        print commandlist #prints to cronlog
        
        #read device list and generate a seperate thread for each device    
        threads = []
        thread_id = 1    
        for line in fh_device_list:
            devicedata = line.split()
            device = Device(devicedata[0], devicedata[1], commandlist, 
                thread_id, uid, pw, db_config)
            device.start()
            threads += [device]
            thread_id += 1
        #Wait for all threads to finish       
        for thread in threads:
            thread.join()

        fh_command_list.close()
        fh_device_list.close()

def run():
    crwl = ConfCrawler()

if __name__ == "__main__": 
    run()