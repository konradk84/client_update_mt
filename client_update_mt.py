import sys, paramiko, re, time, datetime, os, select, configparser


def file_len(ip_list):
    with open(ip_list) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def debug(content):
    print(content)
    time_now = datetime.datetime.now().strftime("%H:%M:%S")
    log_file = open(cfg[config]['DEBUG_FILE'], 'a')
    log_buf = ''
    log_buf = 'log: ' +time_now+ ' : '+content + '\n'
    log_file.write(log_buf)
    log_file.close

def log_error(address, content):
    print(address, content)
    time_now = datetime.datetime.now().strftime("%H:%M:%S")
    log_file = open(cfg[config]['ERROR_FILE'], 'a')
    log_buf = ''
    log_buf = 'log: ' +time_now+ ' : '+address + ' : '+content + '\n'
    log_file.write(log_buf)
    log_file.close
############################################################################ 
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
timeout = 5
#---
#script2 = "/system script add name=script69 source=\"/ip ssh regenerate-host-key;/system scheduler remove numbers=69;/system script remove numbers=script69;\""
script = script[1:]
#script = script[:len(script)-1]
script = script.replace('=/', '="/')

#script = script.strip("\"")
#print('1:', script)
#print('2:', script2)

#input()
#
#Until v6.31: upgrade, after install
##########################################################################
   
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

        debug('############################################\n')
        debug(ip)
        #print('############################################\n')
        print('ip_address: ', ip)
        
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port=port, username=user, password=password, timeout=10)
        
        #print("logged in\n")
        debug("logged in\n")
        
        channel = client.invoke_shell()
        channel_data = bytes()
        while quit_loop == False: #todo: fix that unecessery loop condition
            timeout = 5
            r,w,e = select.select([channel], [], [], timeout)
            if channel in r:
                channel_data += channel.recv(9999)
                buf = channel_data.decode('utf-8')
                #print('buf: ', buf)
                #debug(buf)

                if buf.endswith('] > ') == True:
                    debug(buf)
                    debug('We found prompt')
                    if buf.find('version: ') != -1 and get_version == False:
                        ver_pos = buf.find('version: ')
                        buf = buf.strip( '(stable)' )
                        version = buf[ver_pos+9:ver_pos+15]
                        version = version.strip('(stable)')
                        version = version.strip( ' \r\n' )
                        version = version.strip( 'rc' )
                        #version = version.strip( 'rc') #strip rc versions
                        print('VERSION: ', version)
                        input()
                        get_version = True
                        if version.count('.') > 1:
                            ver_pos = version.rfind('.')
                            #print('ver_pos ostatniej .', ver_pos)
                            #version = version[0:ver_pos] #bez wersji dziesietnie, ladne rozwiazanie
                            version = version[:ver_pos] + version[ver_pos+1:] ##aktualziacja wersji dziesietnej, brzydkie rozwiazanie
                        print('mamy ver: ', version, ', o dlugosci: ', len(version))
                        #ver_content = 'mamy ver: ', version, ', o dlugosci: ', len(version)
                        debug(version)
                    if get_version == False and send_get_version == False:
                        debug('Checking version')
                        channel.send("system resource print\r\n")
                        send_get_version = True
                    #print(get_version, send_get_version)
                    #print("dupa")
                    if get_version == True:
                        debug('Got version, updating')
                        if float(version) >= 6.31:
                            debug('greater or equal 6.31')
                        elif float(version) < 6.31:
                            debug('less 6.31')
                        else:
                            debug('case not know')
                        #channel.send(scheduler+'\r\n')
                        time.sleep(2)
                        #channel.send(script+'\r\n')
                        time.sleep(2)
                        #channel.send(cmd+'\r\n')
                        time.sleep(2)
                        channel_data = bytes()
                        channel.send('quit\r\n')
                        quit_loop = True
                        get_version = False
                        break
                    if buf.find('bad command name') != -1:
                        debug('bad command name')
                        quit_loop = True
                        get_version = False
                        send_get_version = False
                        break   
            print("t/o")
        percent = i / ip_count * 100
        print("---------------- done:  ", int(percent), "% -----------------")

    except paramiko.ssh_exception.AuthenticationException as ssherr:
        debug(str(ssherr))
        #print (ssherr)
        client.close()
    except paramiko.ssh_exception.SSHException as ssherr:
        debug(str(ssherr))
        #print (ssherr)
        client.close()
    except paramiko.ssh_exception.socket.error as ssherr:
        debug(str(ssherr))
        #print (ssherr)
        client.close()
    except paramiko.ssh_exception.BadHostKeyException as ssherr:
        debug(str(ssherr))
        #print (ssherr)
        client.close()
    finally:
        client.close()
#print ("done")
debug("done")
	
	
	
	
	
	
	
	
