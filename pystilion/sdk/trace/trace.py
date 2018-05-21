import os
import traceback
import datetime
import threading
from math import ceil
import binascii
import html
import re

class Trace (object):
    def __init__ (self, trace_folder, app_name, header_template, trailer_template, max_size = 5, max_files = 5):
        self.trace_folder = trace_folder
        self.app_name = app_name
        self.max_size = max_size * 1024 * 1024
        self.max_files = max_files
        with open(header_template) as f:
            self.header = f.read()
            f.closed
        with open(trailer_template) as f:
            self.trailer = f.read()
            f.closed
            
        self.trace_files = []
        self.pattern = re.compile(self.app_name + '_([\d]+).htm')
        self.f = None
        self.lock = threading.Lock()
        self.__setup_trace()
    
    def __setup_trace(self):
        self.__update_file_info()
        self.__remove_file()
        if len(self.trace_files) > 0:
            current_file = os.path.join(self.trace_folder, self.trace_files[-1])
            self.f = open(current_file, 'a')
        else:
            self.__create_file()
    
    def __update_file_info(self):
        # get all files first
        if not os.path.isdir(self.trace_folder):
            os.makedirs(self.trace_folder)
        self.trace_files = [f for f in os.listdir(self.trace_folder) 
                       if os.path.isfile(os.path.join(self.trace_folder, f))]
        # get interested files
        for file in self.trace_files:
            m = self.pattern.match(file)
            if not m:
                self.trace_files.remove(file)        
        # define the sorting keys
        def __file_seq(file):
            m = self.pattern.search(file)
            return int (m.group(1))
        # retrun the sorted file list
        self.trace_files = sorted(self.trace_files, key=__file_seq)
    
    def __create_file(self):
        last_file_seq = 0
        if len(self.trace_files) > 0: 
            pattern = re.compile(self.app_name + '_([\d]+).htm')
            m = pattern.search(self.trace_files[-1])
            last_file_seq =  int (m.group(1))
        self.f = open(os.path.join(self.trace_folder, self.app_name + '_' + str(last_file_seq+1) + '.htm'), 'w')
        self.header = self.header.replace('<app_name></app_name>', self.app_name)
        self.f.write(self.header)
        self.__update_file_info()
    
    def __close_file(self):
        self.f.write(self.trailer)
        self.f.close()
    
    def __remove_file(self):
        if len(self.trace_files) > self.max_files:
            for file in self.trace_files[:len(self.trace_files) - self.max_files]:
                os.remove(os.path.join(self.trace_folder, file))
        self.__update_file_info()
    
    def log(self, summary, detail=None, binary=None, exception=None):
        """
        """
        #add the current thread in front of summary line"""
        summary = '[{}]'.format(threading.current_thread().name) + summary
        #if pass in exception object, extract info to string"""
        if isinstance(exception, Exception):
            exception = "Exception raised {exception_class} ({exception_docstring}): {exception_message}".format(
                    exception_class = exception.__class__,
                    exception_docstring = exception.__doc__,
                    exception_message = str(exception)) + "\n"
            exception += ''.join(traceback.format_stack())
        
        #if no detail presented, but binary or exception presented, duplicate summary into detail"""     
        if detail == None and (binary != None or exception != None):
            detail = summary
        
        if detail == None:
            summary_div = '\t\t<div id="summary">[{}] - {}\n'.format(str(datetime.datetime.now()), html.escape(summary,True))
            detail_div = ''
            detail_trailer = ''
        else:
            summary_div =  '\t\t<div id="summary">[{}] - <a href="javascript://" onclick="toggle(this)">{}</a>\n'.format(str(datetime.datetime.now()), html.escape(summary,True))
            detail_div = '\t\t\t<div id="detail"><ul><pre format="object">' + html.escape(detail,True) + '</pre>\n'
            detail_trailer = '\t\t\t</ul>\n\t\t\t</div>\n'
        summary_trailer = '\t\t</div>\n<!--EOM-->\n'
        
        binary_div = ''
        if binary != None:
            binary_div += '\t\t\t\t<div id="binary"><a href="javascript://" onclick="toggle(this)">binary data</a>\n'
            binary_div += '\t\t\t\t\t<div id="binary_data">\n'
            binary_div += '\t\t\t\t\t<pre format="object">\n'
            binary_div +=  html.escape(Trace.__log_binary(binary), True) + '\n'
            binary_div += '\t\t\t\t\t</pre>\n'
            binary_div += '\t\t\t\t\t</div>\n'
            binary_div += '\t\t\t\t</div>\n'
        
        exception_div=''
        if exception != None:
            exception_div += '\t\t\t\t<div id="exception"><a href="javascript://" onclick="toggle(this)">Exception</a>\n'
            exception_div += '\t\t\t\t\t<div id="exception_data">\n'
            exception_div += '\t\t\t\t\t<pre format="object">\n'
            exception_div +=  html.escape(exception,True) + '\n'
            exception_div += '\t\t\t\t\t</pre>\n'
            exception_div += '\t\t\t\t\t</div>\n'
            exception_div += '\t\t\t\t</div>\n'
        output = summary_div + detail_div + binary_div + exception_div + detail_trailer + summary_trailer    
        
        #need to get lock to write to file
        self.lock.acquire()
        try:
            self.f.write(output)
            self.f.flush()
            if os.path.getsize(self.f.name) > self.max_size:
                self.__close_file()
                self.__create_file()
                self.__remove_file()
        finally:
            self.lock.release()
    
    @staticmethod
    def __log_binary(binary):
        output = []
        # i for per row, j for per column
        for i in range(0, ceil(len(binary)/16)):
            output.append( str(i*16).zfill(5) )
            output.append( '(0x{})  '.format(str(hex(i*16))[2:].zfill(4)) )
            # hexdecimal part
            for j in range(0, 16):
                p = i * 16 + j
                if p < len(binary):
                    output.append( binascii.hexlify(binary[p:p+1]).decode('ascii') )
                else:
                    output.append('  ')
                output.append(' ')
            output.append('   ')
            # ascii part
            for j in range(0, 16):
                p = i*16+j
                if p >= len(binary): break
                if (binary[p:p+1] < b'\x20' or binary[p:p+1] > b'\x7E'): 
                    output.append('.')
                else: 
                    output.append( binary[p:p+1].decode('ascii') )
            output.append('\n')
        return ''.join(output)


    