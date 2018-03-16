import binascii


class Bitmap(object):
    def __init__(self, value=None, field_def={}):
        self.fields = {}
        self.field_def = field_def
        if value != None:
            self.from_msg(value)
    
    def set_field(self,name,value):
        self.fields[name] = Field(name, value, self.field_def[name])
    
    def get_field(self,name):
        if name in self.fields.keys():
            return self.fields[name].get_value()
        else: 
            return None
    
    def clear_field(self,name):
        '''Remove a field in bitmap message'''
        del(self.fields[name])
 
    def from_msg(self, msg):
        bitmap = [0]
        p = 0
        #Parse Bitmap
        while True: 
            bitmap_byte = Bitmap.__parse_bitmap(msg[p:p+8])
            bitmap.extend(bitmap_byte)
            p += 8
            if bitmap_byte[0] == 0: 
                break
        #Parse fields
        for i in range(2,len(bitmap)):
            if bitmap[i] == 1:
                len_len = self.field_def[i]['len_format'].count('L')
                if len_len > 0: 
                    field_len = int(msg[p:p+len_len])
                    p += len_len
                else:
                    field_len = self.field_def[i]['max_len']
                self.set_field(i, msg[p:p+field_len])
                p += field_len
    
    def to_msg(self, msg):
        '''
        implemented in the child classes
        '''
        pass
    
    @staticmethod
    def __parse_bitmap(bitmap_byte):
        '''
        Parse 8 bytes of bitmap into a int list
        '''
        result=''
        for i in bitmap_byte:
            result+=bin(i)[2:].zfill(8)
        return list(map(int,result))
    
    def __str__(self):
        output = ''
        for f in sorted(self.fields.keys()):
            output += str(self.fields[f])
        return output

class Field(object):
       
    def __init__(self, name, value, field_def, coding='latin'):
        self.name=name
        self.data_format=field_def['data_format']
        self.len_format=field_def['len_format']
        self.max_len=field_def['max_len']
        self.desc=field_def['desc']
        self.coding = coding
        self.value = None
        if value is not None:
            self.set_value(value)
            
    def set_value(self,value):
        if type(value) is bytes:
            self.value = value
        if type(value) is str:
            self.value = value.encode(self.coding)
    
    def get_value(self):
        if self.coding.count('b') == 0:
                return self.value.decode(self.coding)
        else:
                return self.value
    
    def get_binary_value(self):
        return self.value

    def to_msg(self):
        if self.len_format == "F":
            return bytearray(self.value)
        else:
            len_len = self.len_format.count("L")
            len_field=str(len(self.value))  
            result=bytearray(len_field.zfill(len_len).encode(self.coding))
            result.extend(bytearray(self.value))
            return result
    
    def __str__(self): 
        col1 = self.len_format.ljust(7)
        col2 = self.data_format.ljust(4)
        if self.len_format.count("L") > 0: 
            col3 = ('.' + str(self.max_len)).rjust(7)
        else: 
            col3 = str(self.max_len).rjust(7)
        output = '[{}{}{}]'.format(col1, col2, col3) + str(self.name).center(6, ' ')
        if self.data_format != 'b':
            output += '[{}]\n'.format(self.value.decode(self.coding))
        else:
            output += '[Ox {}]\n'.format(binascii.hexlify(self.value).decode(self.coding))
        return output
        
if __name__ == "__main__":
    msg=b'\xf2\x3c\x46\x80\x21\xe0\x80\x20\x00\x00\x00\x00\x00\x00\x00\x22'
    msg+=b'\x31\x36\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a' 
    msg+=b'\x30\x30\x33\x30\x30\x30'
    msg+=b'\x30\x30\x30\x30\x30\x30\x30\x30\x35\x30\x30\x30'
    msg+=b'\x30\x38\x32\x30\x31\x33\x32\x36\x32\x39'
    msg+=b'\x37\x32\x30\x34\x36\x36'
    msg+=b'\x31\x34\x32\x36\x32\x39'
    msg+=b'\x30\x38\x32\x30'
    msg+=b'\x32\x35\x31\x32'
    msg+=b'\x30\x30\x30\x30'
    msg+=b'\x30\x35\x31'
    msg+=b'\x30\x30\x31'
    msg+=b'\x30\x30'
    msg+=b'\x33\x34\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a'
    msg+=b'\x32\x30\x31'
    msg+=b'\x30\x32\x34\x37\x30\x30\x30\x32'
    msg+=b'\x30\x32\x34\x37\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20'
    msg+=b'\x30\x32\x34\x37\x3a\x4e\x65\x77\x63\x61\x73\x74\x6c\x65\x20\x55\x4c\x20\x20\x20\x20\x20\x20\x4e\x65\x77\x63\x61\x73\x74\x6c\x65\x20\x55\x4c\x20\x20\x20\x47\x42'
    msg+=b'\x38\x32\x36'
    msg+=b'\x30\x31\x30\x7e\x30\x35\x31\x30\x30\x30\x30\x31\x30'
    msg+=b'\x30\x31\x35\x35\x31\x30\x31\x30\x31\x35\x31\x31\x30\x34\x43\x31\x30\x31'
    msg+=b'\x30\x30\x30\x31\x37\x30\x41\x1c\x04\x00\x00\x00\x00\x00\x33\x31\x31\x30\x32\x34\x37\x30\x30\x30\x32\x30\x38\x32\x30\x31\x35\x30\x32\x30\x30\x39\x39\x34\x34\x38\x39\x30\x30\x30\x30\x34\x34\x30\x30\x35\x2a\x2a\x2a\x2a\x2a\x32\x35\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x58\x58\x31\x20\x31\x58\x58\x20\x20\x38\x32\x36\x20\x20\x20\x20\x20\x20\x20\x20\x30\x30\x30\x36\x34\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a\x2a'
    
    field_def={
        2:  {'data_format':'n',    'len_format':'LL',  'max_len':19,   'desc':'Field 2 - Primary Account Number (PAN)'},
        3:  {'data_format':'n',    'len_format':'F',   'max_len':6,    'desc':'Field 3 - Processing Code'},
        4:  {'data_format':'n',    'len_format':'F',   'max_len':12,   'desc':'Field 4 - Amount Transaction'},
        5:  {'data_format':'n',    'len_format':'F',   'max_len':12,   'desc':'Field 5 - Amount Settlement'},
        7:  {'data_format':'n',    'len_format':'F',   'max_len':10,   'desc':'Field 7 - Transmission Date and Time'},
        9:  {'data_format':'n',    'len_format':'F',   'max_len':8,    'desc':'Field 9 - Conversion Rate, Settlement'},
        11: {'data_format':'n',    'len_format':'F',   'max_len':6,    'desc':'Field 11 - Systems Trace Audit Number'},
        12: {'data_format':'n',    'len_format':'F',   'max_len':6,    'desc':'Field 12 - Time, Local Transaction'},
        13: {'data_format':'n',    'len_format':'F',   'max_len':4,    'desc':'Field 13 - Date, Local Transaction'},
        14: {'data_format':'n',    'len_format':'F',   'max_len':4,    'desc':'Field 14 - Date, Expiration'},
        15: {'data_format':'n',    'len_format':'F',   'max_len':4,    'desc':'Field 15 - Date, Settlement'},
        16: {'data_format':'n',    'len_format':'F',   'max_len':4,    'desc':'Field 16 - Date, Conversion'},
        18: {'data_format':'n',    'len_format':'F',   'max_len':4,    'desc':'Field 18 - Merchant Type'},
        22: {'data_format':'n',    'len_format':'F',   'max_len':3,    'desc':'Field 22 - POS Entry Mode'},
        23: {'data_format':'n',    'len_format':'F',   'max_len':3,    'desc':'Field 23 – Card Sequence Number'},
        25: {'data_format':'n',    'len_format':'F',   'max_len':2,    'desc':'Field 25 - POS Condition Code'},
        26: {'data_format':'n',    'len_format':'F',   'max_len':2,    'desc':'Field 26 - POS PIN Capture Code'},
        27: {'data_format':'n',    'len_format':'F',   'max_len':1,    'desc':'Field 27 - Authorization ID Response Length'},
        28: {'data_format':'x+n',  'len_format':'F',   'max_len':9,    'desc':'Field 28 - Amount, Transaction Fee'},
        29: {'data_format':'x+n',  'len_format':'F',   'max_len':9,    'desc':'Field 29 - Amount, Settlement Fee'},
        30: {'data_format':'x+n',  'len_format':'F',   'max_len':9,    'desc':'Field 30 - Amount, Transaction Processing Fee'},
        31: {'data_format':'x+n',  'len_format':'F',   'max_len':9,    'desc':'Field 31 - Amount, Settle Processing Fee'},
        32: {'data_format':'n',    'len_format':'LL',  'max_len':11,   'desc':'Field 32 - Acquiring Institution ID Code'},
        33: {'data_format':'n',    'len_format':'LL',  'max_len':11,   'desc':'Field 33 - Forwarding Institution ID Code'},
        35: {'data_format':'z',    'len_format':'LL',  'max_len':37,   'desc':'Field 35 - Track 2 Data'},
        37: {'data_format':'anp',  'len_format':'F',   'max_len':12,   'desc':'Field 37 - Retrieval Reference Number'},
        38: {'data_format':'anp',  'len_format':'F',   'max_len':6,    'desc':'Field 38 - Authorization ID Response'},
        39: {'data_format':'an',   'len_format':'F',   'max_len':2,    'desc':'Field 39 - Response Code'},
        40: {'data_format':'n',    'len_format':'F',   'max_len':3,    'desc':'Field 40 - Service Restriction Code'},
        41: {'data_format':'ans',  'len_format':'F',   'max_len':8,    'desc':'Field 41 - Card Acceptor Terminal ID'},
        42: {'data_format':'ans',  'len_format':'F',   'max_len':15,   'desc':'Field 42 - Card Acceptor ID Code'},
        43: {'data_format':'ans',  'len_format':'F',   'max_len':40,   'desc':'Field 43 - Card Acceptor Name Location'},
        44: {'data_format':'ans',  'len_format':'LL',  'max_len':25,   'desc':'Field 44 - Additional Response Data'},
        45: {'data_format':'ans',  'len_format':'LL',  'max_len':76,   'desc':'Field 45 - Track 1 Data'},
        48: {'data_format':'ans',  'len_format':'LLL', 'max_len':999,  'desc':'Field 48 - Additional Data'},
        49: {'data_format':'an',   'len_format':'F',   'max_len':3,    'desc':'Field 49 - Currency Code, Transaction'},
        50: {'data_format':'an',   'len_format':'F',   'max_len':3,    'desc':'Field 50 - Currency Code, Settlement'},
        52: {'data_format':'b',    'len_format':'F',   'max_len':8,    'desc':'Field 52 - PIN Data'},
        53: {'data_format':'b',    'len_format':'F',   'max_len':48,   'desc':'Field 53 - Security Related Control Information'},
        54: {'data_format':'an',   'len_format':'LLL', 'max_len':120,  'desc':'Field 54 - Additional Amounts'},
        56: {'data_format':'n',    'len_format':'LLL', 'max_len':4,    'desc':'Field 56 - Message Reason Code'},
        57: {'data_format':'n',    'len_format':'F',   'max_len':3,    'desc':'Field 57 - Authorization Life-cycle Code'},
        58: {'data_format':'np',   'len_format':'LL',  'max_len':11,   'desc':'Field 58 - Authorizing Agent Institution'},
        59: {'data_format':'ans',  'len_format':'LLL', 'max_len':500,  'desc':'Field 59 - Echo Data'},
        66: {'data_format':'n',    'len_format':'F',   'max_len':1,    'desc':'Field 66 - Settlement Code'},
        67: {'data_format':'n',    'len_format':'F',   'max_len':2,    'desc':'Field 67 - Extended Payment Code'},
        70: {'data_format':'n',    'len_format':'F',   'max_len':3,    'desc':'Field 70 - Network Management Information Code'},
        73: {'data_format':'n',    'len_format':'F',   'max_len':6,    'desc':'Field 73 - Date, Action'},
        74: {'data_format':'n',    'len_format':'F',   'max_len':10,   'desc':'Field 74 - Credits, Number'},
        75: {'data_format':'n',    'len_format':'F',   'max_len':10,   'desc':'Field 75 - Credits, Reversal Number'},
        76: {'data_format':'n',    'len_format':'F',   'max_len':10,   'desc':'Field 76 - Debits, Number'},
        77: {'data_format':'n',    'len_format':'F',   'max_len':10,   'desc':'Field 77 - Debits, Reversal Number'},
        78: {'data_format':'n',    'len_format':'F',   'max_len':10,   'desc':'Field 78 - Transfer, Number'},
        79: {'data_format':'n',    'len_format':'F',   'max_len':10,   'desc':'Field 79 - Transfer, Reversal Number'},
        80: {'data_format':'n',    'len_format':'F',   'max_len':10,   'desc':'Field 80 - Inquiries, Number'},
        81: {'data_format':'n',    'len_format':'F',   'max_len':10,   'desc':'Field 81 - Authorizations, Number'},
        82: {'data_format':'n',    'len_format':'F',   'max_len':12,   'desc':'Field 82 - Credits, Processing Fee Amount'},
        83: {'data_format':'n',    'len_format':'F',   'max_len':12,   'desc':'Field 83 - Credits, Transaction Fee Amount'},
        84: {'data_format':'n',    'len_format':'F',   'max_len':12,   'desc':'Field 84 - Debits, Processing Fee Amount'},
        85: {'data_format':'n',    'len_format':'F',   'max_len':12,   'desc':'Field 85 - Debits, Transaction Fee Amount'},
        86: {'data_format':'n',    'len_format':'F',   'max_len':16,   'desc':'Field 86 - Credits, Amount'},
        87: {'data_format':'n',    'len_format':'F',   'max_len':16,   'desc':'Field 87 - Credits, Reversal Amount'},
        88: {'data_format':'n',    'len_format':'F',   'max_len':16,   'desc':'Field 88 - Debits, Amount'},
        89: {'data_format':'n',    'len_format':'F',   'max_len':16,   'desc':'Field 89 - Debits, Reversal Amount'},
        90: {'data_format':'n',    'len_format':'F',   'max_len':42,   'desc':'Field 90 - Original Data Elements'},
        91: {'data_format':'an',   'len_format':'F',   'max_len':1,    'desc':'Field 91 - File Update Code'},
        95: {'data_format':'an',   'len_format':'F',   'max_len':42,   'desc':'Field 95 - Replacement Amounts'},
        97: {'data_format':'x+n',  'len_format':'F',   'max_len':17,   'desc':'Field 97 - Amount, Net Settlement'},
        98: {'data_format':'ans',  'len_format':'F',   'max_len':25,   'desc':'Field 98 - Payee'},
        100:{'data_format':'n',    'len_format':'LL',  'max_len':11,   'desc':'Field 100 - Receiving Institution ID Code'},
        101:{'data_format':'ans',  'len_format':'LL',  'max_len':17,   'desc':'Field 101 - File Name'},
        102:{'data_format':'ans',  'len_format':'LL',  'max_len':28,   'desc':'Field 102 - Account Identification 1'},
        103:{'data_format':'ans',  'len_format':'LL',  'max_len':28,   'desc':'Field 103 - Account Identification 2'},
        118:{'data_format':'n',    'len_format':'LLL',  'max_len':10,   'desc':'Field 118 - Payments, Number'},
        119:{'data_format':'n',    'len_format':'LLL',  'max_len':10,   'desc':'Field 119 - Payments, Reversal Number'},
        123:{'data_format':'an',   'len_format':'LLL',  'max_len':15,   'desc':'Field 123 - POS Data Code'},
        127:{'data_format':'ans',  'len_format':'LLLLLL',  'max_len':999999,   'desc':'Field 127 - Realtime Private Field'}
    }
    
    bb=Bitmap(msg,field_def)
    print (bb)
    bb.clear_field(25)
    print (bb)

