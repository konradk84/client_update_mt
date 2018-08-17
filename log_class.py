import datetime

class Log():
    
    def __init__(self, file_out):
        self.log_file = open(file_out, 'a')
        #print('file opened')
        self.buf = ''
            
    def __del__(self):
        log_file = self.__init__
        self.log_file.close
        #print('file closed')

    def debug(self, content):
        #log_file = self.__init__
        self.time_now = datetime.datetime.now().strftime("%H:%M:%S")
        self.content = content
        buf = self.time_now + ' : ' + self.content + '\n'
        print(buf)
        self.log_file.write(buf)
        #self.log_file.close
    def error_log(self, address, content):
        log_file = self.__init__
        self.time_now = datetime.datetime.now().strftime("%H:%M:%S")
        self.address = address
        self.content = content
        buf = self.time_now + ' : ' + address  + self.content + '\n'
        self.log_file.write(buf)
        #file = file + '_' + cfg[config]['ERROR_FILE']


#ob = Log('ip.txt', 'out.test')
#print('dlugosc', ob.file_len('ip.txt'))
#ob.write_to_log('asd')

