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
    
    #Todo:  1. The App hangs. On some Devices (random) the commands are not 
            executet, the telnet session however has been established. This
            causes the app to hang! This does not seem to be a problem with 
            a certain device. Sometimes it affects more othertime less devices.

            Narrowed it down to the first command which seems always to be run.
            However the second command hangs in thin air. Regarding ACS Logs it 
            is never executed and is also never printed to stout.

            It does also not seem to be a timing issue (sleep) !!!

"""
from cc_device import Device

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

        #timestamp = datetime.datetime.now()
        #timestamp = timestamp.strftime("%Y_%m_%d_%H_%M")
        #print timestamp

        uid = 'confcrwl'
        pw = 'N3bu1aOn3!'

        #Read device- and command lists
        fh_device_list = open ('./conf/devicelist', 'r')
        fh_command_list = open ('./conf/commandlist', 'r')

        commandlist = []
        for command in fh_command_list:
            commandlist.append(command)
        print commandlist

        #commandlis = ['terminal length 0', 'sh run']
        #print commandlis

        #Generate a seperate thread for each device       
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