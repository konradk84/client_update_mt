import sys, paramiko, re, time, datetime, os, select, configparser
from log_class import *
from version_mt_class import *

channel_data = bytes()
buf = ''

cfg = configparser.ConfigParser()
cfg.read('config.ini')
#check arguments
if len(sys.argv) < 3:
    print('''\nToo few arguments. Usage: client_update_mt.py <config_section> <ip_list> ''')
    #config = sys.argv[1]
    #cmd = cfg[config]['COMMAND']
    #print(cmd)
    exit()

config = sys.argv[1]
#ip_list = cfg[config]['IP_FILE']
ip_list = sys.argv[2]
user = cfg[config]['LOGIN']
password = cfg[config]['PASSWORD']
port = cfg[config]['PORT']
scheduler = cfg[config]['SCHEDULER']
script = cfg[config]['SCRIPT']
cmd = cfg[config]['COMMAND']
cmd2 = cfg[config]['COMMAND2']
timeout = 5
#script2 = "/system script add name=script69 source=\"/ip ssh regenerate-host-key;/system scheduler remove numbers=69;/system script remove numbers=script69;\""
script = script[1:]
script = script.replace('=/', '="/')

def file_len(ip_list):
    with open(ip_list) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

file = ip_list.strip('.txt')
file_debug = file + '_' + cfg[config]['DEBUG_FILE']
file_error = file + '_' + cfg[config]['ERROR_FILE']
log = Log(file_debug, file_error)

print(ip_list)
ip_count = file_len(ip_list) #todo: check len, if 0 then exit
file_in = open(ip_list, 'r')
#file_in = open(sys.argv[2])
for i, line in enumerate(file_in):
    try:
        quit_loop = False
        prompt = False
        get_version = False
        send_get_version = False
        buf_ip = line
        ip = buf_ip.strip( '\n' )

        log.debug('############################################\n')
        log.debug(ip)
        #log.error_log(ip, 'test')
        #print('############################################\n')
        print('ip_address: ', ip)
        
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port=port, username=user, password=password, timeout=10)
        
        #print("logged in\n")
        log.debug("logged in\n")
        now = int(time.time())
        channel = client.invoke_shell()
        channel_data = bytes()
        while quit_loop == False: #todo: fix that unecessery loop condition
            timeout = 5
            r,w,e = select.select([channel], [], [], timeout)
            if channel in r:
                channel_data += channel.recv(9999)
                buf = channel_data.decode('utf-8')
                #print('buf: ', buf)
                #log.debug(buf)

                if buf.endswith('] > ') == True:
                    log.debug(buf)
                    log.debug('We found prompt')
                    if buf.find('version: ') != -1 and get_version == False:
                        try:
                            version = Version()
                            version = version.find_version(buf)
                        except:
                            log.log_error(ip, " exception occured: \r\n" + "-------------- buf start -------------\r\n" + buf + '\r\n-------------- buf end -------------')
                            quit_loop = True
                            get_version = False
                            send_get_version = False
                            client.close()
                        #print('version object method returns: ')
                        #print('version: ', version, ' version len: ', len(version))
                        get_version = True
                        #print('mamy ver: ', version, ', o dlugosci: ', len(version))
                        #input()
                        log.debug(version)
                    if get_version == False and send_get_version == False:
                        log.debug('Checking version')
                        channel.send("system resource print\r\n")
                        send_get_version = True
                    if get_version == True:
                        log.debug('Got version, updating')
                        if float(version) >= 6.31 and float(version) != 6.427:
                            log.debug('greater or equal 6.31')
                            channel.send(scheduler+'\r\n')
                            time.sleep(2)
                            channel.send(script+'\r\n')
                            time.sleep(2)
                            channel.send(cmd+'\r\n')
                            time.sleep(2)
                        elif float(version) < 6.31:
                            log.debug('less 6.31')
                            if float(version) >= 6.0:
                                log.debug('greater or equal 6.0')
                                channel.send(scheduler+'\r\n')
                                time.sleep(2)
                                channel.send(script+'\r\n')
                                time.sleep(2)
                            channel.send(cmd2+'\r\n')
                            time.sleep(2)
                        else:
                            log.debug('case not handled')
                            log.error_log(ip, buf+'\r\ncase not handled\r\n')
                        channel_data = bytes()
                        channel.send('quit\r\n')
                        quit_loop = True
                        get_version = False
                        break
                    if buf.find('bad command name') != -1:
                        log.debug('bad command name')
                        log.error_log(ip, buf+'\r\nbad command name\r\n')
                        quit_loop = True
                        get_version = False
                        send_get_version = False
                        break   
            log.debug("t/o")
            if(int(time.time()) > now + 60):
                log.debug('timeout 60 s')
                log.error_log(ip, 'timeout 60 s')
                quit_loop = True
                get_version = False
                send_get_version = False
                break   
        percent = i / ip_count * 100
        print("---------------- done:  ", int(percent), "% -----------------")

    except paramiko.ssh_exception.AuthenticationException as ssherr:
        log.debug(str(ssherr))
        #print (ssherr)
        client.close()
    except paramiko.ssh_exception.SSHException as ssherr:
        log.debug(str(ssherr))
        #print (ssherr)
        client.close()
    except paramiko.ssh_exception.socket.error as ssherr:
        log.debug(str(ssherr))
        #print (ssherr)
        client.close()
    except paramiko.ssh_exception.BadHostKeyException as ssherr:
        log.debug(str(ssherr))
        #print (ssherr)
        client.close()
    finally:
        client.close()
#print ("done")
log.debug("done")
	
	
	
	
	
	
	
	
