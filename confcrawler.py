#!/usr/bin/python
"""
    Name:     confcrawler
    Version:  RC 0.0.1 
    Author:   Antares
    Modified: 07.10.13
    
    This script is run by a cron job. It retrieves configurations from cisco
    devices by connecting to them over telnet. These devices are stored in a 
    seperate file called ./devicelist. It has the possibility to execute
    different commands which are stored in a file called ./commandlist.
    The configs are stored in the directory ./device_configs by appending the
    date to the name of the device.

    Files:  ./device_configs/:  stores pulled configurations
            ./conf/commandlist: contains commands (1 each line)
            ./conf/devicelist:  stores devices (hostname ip)
            ./cc_globals:       contains global variables   
            ./cc_device:        device class 
            ./j_connect:        connect module (telnet)

    Install cronjob :   
        1. crontab -e
        2. 55 23 * * * /home/tbsadmin/projects/confcrawler/confcrawler.py 
            > /home/tbsadmin/cronlog 2>&1
 
    #Todo: 
"""
import os
from cc_device import Device
from cc_globals import Globals

class ConfCrawler(object):
    """ Main class

    Reads device and command list. For each device a new thread is created.
    """
    def __init__(self):
        
        #Credentials
        uid = 'confcrwl'
        pw = 'N3bu1aOn3!'

        #Setting global variables and paths (stored in cc_globals)
        rootdir = os.path.dirname(__file__)
        Globals.dir_rootdir = rootdir
        Globals.dir_deviceconfig = os.path.join(rootdir, 'device_configs/')
        Globals.file_devicelist = os.path.join(rootdir, 'conf/devicelist')
        Globals.file_commandlist = os.path.join(rootdir, 'conf/commandlist')

        #Global = Globals()
        #Global.print_globals()

        fh_device_list = open (Globals.file_devicelist, 'r')
        fh_command_list = open (Globals.file_commandlist, 'r')
        
        #read command list
        commandlist = []
        for command in fh_command_list:
            commandlist.append(command)
        print commandlist
        
        #read device list and generate a seperate thread for each device       
        threads = []
        thread_id = 1    
        for line in fh_device_list:
            devicedata = line.split()
            device = Device(devicedata[0], devicedata[1], commandlist, 
                thread_id, uid, pw)
            device.start()
            threads += [device]
            thread_id += 1
        #Wait for all threads to finish       
        for thread in threads:
            thread.join()

def run():
    crwl = ConfCrawler()

if __name__ == "__main__": 
    run()