"""
    Name:     confcrawler
    Version:  Dev. 0.0.1 
    Author:   Memleak13
    Modified: 03.10.13
    
    This script is run by a cron job. It retrieves configurations from cisco
    devices by connecting to them over telnet. These devices are stored in a 
    seperate file called ./devicelist. It has the possibility to execute
    different commands which are stored in a file called ./commandlist.
    The configs are stored in the directory ./device_configs by appending the
    date to the name of the device.
    
    #Todo:

"""
import datetime
from j_connect import TnCiscoAccess

class ConfCrawler(object):
    """ Main class

    Reads device and command list. For each device a new thread is created.
    """
    def __init__(self):
        
        #fh = open('./output', 'w')
        #test = TnCiscoAccess('10.10.10.11', 'csw01SHR', 'rconfig', 'N3bu1a!')
        #test.no_enable()
        #commands = ['terminal length 0', 'sh run']
        #fh.write(test.run_command(commands))

        timestamp = datetime.datetime.now()
        timestamp = timestamp.strftime("%Y_%m_%d_%H_%M")
        
def run():
    crwl = ConfCrawler()

if __name__ == "__main__": 
    run()