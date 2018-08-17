import datetime

class Log():
    
    def __init__(self, file_in, file_out):
        file = file_in.strip('.txt')
        file = file + '_' + file_out
        self.log_file = open(file, 'a')
        #print('file opened')
        self.buf = ''
            
    def __del__(self):
        log_file = self.__init__
        self.log_file.close
        #print('file closed')
            
    def file_len(self, file_in):
        with open(file_in) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

    def write_to_log(self, content):
        log_file = self.__init__
        self.time_now = datetime.datetime.now().strftime("%H:%M:%S")
        self.content = content
        buf = 'log: ' +self.time_now+ ' : ' +self.content + '\n'
        self.log_file.write(buf)
        #self.log_file.close


ob = Log('ip.txt', 'out.test')
print('dlugosc', ob.file_len('ip.txt'))
ob.write_to_log('asd')

