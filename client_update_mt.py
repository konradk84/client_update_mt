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
prompt = False

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
ip_list = cfg[config]['IP_FILE']
user = cfg[config]['LOGIN']
password = cfg[config]['PASSWORD']
port = cfg[config]['PORT']
scheduler = cfg[config]['SCHEDULER']
#cmd = cfg[config]['COMMAND']
#to = cfg['DEFAULT]']['TIMEOUT'] #TODO
timeout = 5
#---
#script = "/system script add name=script69 source=\"/ip ssh regenerate-host-key;/system scheduler remove numbers=69;/system script remove numbers=script69;\"" + "\r\n" + "\"\""
script = "/system script add name=script69 source=\"/ip ssh regenerate-host-key;/system scheduler remove numbers=69;/system script remove numbers=script69;\""

#script = bytearray()
#script.append('a')
b = bytearray(script, "utf8")
b[67:68] = b'\x0D'
b[68:69] = b'\x0A'
b.append(0x0D)
b.append(0x0A)
#script.append('b')

print("b: ", b)

input()

##########################################################################
   
print(ip_list)
ip_count = file_len(ip_list) #todo: check len, if 0 then exit
file_in = open(ip_list, 'r')
for i, line in enumerate(file_in):
    try:
        quit_loop = False
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
            r,w,e = select.select([channel], [], [], timeout)
            if channel in r:
                channel_data += channel.recv(9999)
                buf = channel_data.decode('utf-8')
                print('buf: ', buf)
                debug(buf)
                if buf.endswith('] > ') == True:
                    debug('We found prompt, sending scheduler')
                    #channel.send(cmd+'\r\n')
                    #channel.send(scheduler+'\r\n')
                    time.sleep(2)
                    channel.send(script+'\r\n')
                    print('b: ', script)
                    channel_data = bytes()
                    time.sleep(2)
                    channel.send('quit\r\n')
                    quit_loop = True
                    break     
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
	
	
	
	
	
	
	
	
