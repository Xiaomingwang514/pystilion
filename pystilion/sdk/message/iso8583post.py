from pystilion.sdk.message.bitmap import Field, Bitmap


class Iso8583Post(Bitmap):
    ''' Postilion ISO8583 message
    
    Create a Postilion ISO8583 message
    
    Attributes:
        MTI: messsage type indicator
        fields: a dict storing field object
        private: storing private field 
        field_def: definition of fields in 127
    '''
    def __init__(self, value=None):
        ''' Create a Postilion message object with optional value 
        
        Args: value is a optional for building a private field, is should be bytes
        '''
        self.MTI = ''
        self.fields = {}
        self.private = None
        super(Iso8583Post,self).__init__(value,Iso8583Post.field_def)
 
    def from_msg(self, msg):
        ''' Parse data to build iso8583 Postilion message 
        
        It is called by Bitmap __init__, it is also construct private field
         
        Args: msg in bytes containing the whole message but excluding header.
        '''
        #Parse MTI 
        p=0
        self.MTI=msg[p:p+4].decode('ascii')
        p+=4
        #Parse fields 
        super(Iso8583Post,self).from_msg(msg[p:])
        #Parse private fields
        if 127 in self.fields.keys():
            self.private=Private(self.fields[127].get_binary_value())
            self.fields[127] = self.private
            
    def to_msg(self):
        ''' Return a bytearray for the iso8583 message with 16 bytes binary bitmap and 2 bytes binary header'''
        data = bytearray()
        result = bytearray()    
        bitmap_str="1"
        for i in range (2,129):
            if i in self.fields.keys():
                bitmap_str+='1'
            else:
                bitmap_str+='0'
        data.extend(self.MTI.encode('ascii'))
        for i in range(0,len(bitmap_str),8):
            data.append(int(bitmap_str[i:i+8],2))
        for i in range(1,len(bitmap_str)):
            if bitmap_str[i]=='1':
                data.extend(self.fields[i+1].to_msg())
        len_field=len(data)
        result.extend(len_field.to_bytes(2, byteorder='big', signed=False))
        result.extend(data)
        return result
    
    def __str__(self):
        output = "MTI:\t" + self.MTI + '\n'
        output += super(Iso8583Post,self).__str__()
        return output
    
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
        127:{'data_format':'b+ans',  'len_format':'LLLLLL',  'max_len':999999,   'desc':'Field 127 - Realtime Private Field'}
    }


class Private(Bitmap):
    ''' Private fields in 127
    
    Create a Postilion private field in bitmap 127
    
    Attributes:
        fields: a dict storing field object
        sd: storing structure data object 
        field_def: definition of fields in 127
    '''
    
    def __init__(self, value=None):
        ''' Create a private field object with optional value 
        
        Args: value is a optional for building a private field
        '''
        self.fields = {}
        self.sd = None
        super(Private,self).__init__(value,Private.field_def)
    
    def from_msg(self, msg):
        ''' Parse message to build private field object
        
        It is called by Bitmap __init__, it is also construct structure data.
         
        Args: msg in bytes containing the whole private field. 
        '''
        super(Private,self).from_msg(msg)
        if 22 in self.fields.keys():
            self.sd = Sd(self.fields[22].get_value())
            self.fields[22] = self.sd
                        
    def to_msg(self):
        ''' Return a bytearray for the private field with 8 bytes binary bitmap and ASCII length'''
        data = bytearray()
        result = bytearray()
        bitmap_str = "0"
        for i in range (2,64):
            if i in self.fields.keys():
                bitmap_str += '1'
            else:
                bitmap_str += '0'       
        for i in range(0,len(bitmap_str),8):
            data.append(int(bitmap_str[i:i+8],2))
        for i in range(1,len(bitmap_str)):
            if bitmap_str[i] == '1':
                data.extend(self.fields[i+1].to_msg())
        len_field = str(len(data))  
        result.extend(len_field.zfill(6).encode('ascii'))
        result.extend(data)
        return result
    
    def __str__(self):
        output = '[  Private Fields  ] 127. \n'
        output += super(Private,self).__str__()
        return output
    
    field_def={
        2:  {'data_format':'ans',    'len_format':'LL',    'max_len':32,   'desc':'Field 127.2 - Switch Key'},
        3:  {'data_format':'ans',    'len_format':'F',     'max_len':48,   'desc':'Field 127.3 - Routing Information'},
        4:  {'data_format':'ans',    'len_format':'F',     'max_len':22,   'desc':'Field 127.4 - POS Data'},
        5:  {'data_format':'ans',    'len_format':'F',     'max_len':73,   'desc':'Field 127.5 - Service Station Data'},
        6:  {'data_format':'an',     'len_format':'F',     'max_len':2,    'desc':'Field 127.6 - Authorization Profile'},
        7:  {'data_format':'ans',    'len_format':'LL',    'max_len':70,   'desc':'Field 127.7 - Check Data'},
        8:  {'data_format':'ans',    'len_format':'LLL',   'max_len':999,  'desc':'Field 127.8 - Retention Data'},
        9:  {'data_format':'ans',    'len_format':'LLL',   'max_len':999,  'desc':'Field 127.9 - Additional Node Data'},
        10: {'data_format':'n',      'len_format':'F',     'max_len':3,    'desc':'Field 127.10 - CVV2'},
        11: {'data_format':'ans',    'len_format':'LL',    'max_len':32,   'desc':'Field 127.11 - Original Key'},
        12: {'data_format':'ans',    'len_format':'LL',    'max_len':25,   'desc':'Field 127.12 - Terminal Owner'},
        13: {'data_format':'ans',    'len_format':'F',     'max_len':17,   'desc':'Field 127.13 - POS Geographic Data'},
        14: {'data_format':'ans',    'len_format':'F',     'max_len':8,    'desc':'Field 127.14 - Sponsor Bank'},
        15: {'data_format':'ans',    'len_format':'LL',    'max_len':29,   'desc':'Field 127.15 - Address Verification Data'},
        16: {'data_format':'a',      'len_format':'F',     'max_len':1,    'desc':'Field 127.16 - Address Verification Result'},
        17: {'data_format':'ans',    'len_format':'LL',    'max_len':50,   'desc':'Field 127.17 - Cardholder Information'},
        18: {'data_format':'ans',    'len_format':'LL',    'max_len':50,   'desc':'Field 127.18 - Validation data'},
        19: {'data_format':'ans',    'len_format':'F',     'max_len':31,   'desc':'Field 127.19 - Bank details'},
        20: {'data_format':'n',      'len_format':'F',     'max_len':8,    'desc':'Field 127.20 - Originator/Authorizer date settlement'},
        21: {'data_format':'ans',    'len_format':'LL',    'max_len':12,   'desc':'Field 127.21 - Record identification'},
        22: {'data_format':'ans',    'len_format':'LLLLL', 'max_len':99999,'desc':'Field 127.22 - Structured data'},
        23: {'data_format':'ans',    'len_format':'F',     'max_len':253,  'desc':'Field 127.23 - Payee name and address'},
        24: {'data_format':'ans',    'len_format':'LL',    'max_len':28,   'desc':'Field 127.24 - Payee reference'},
        25: {'data_format':'ans',    'len_format':'LLLL',  'max_len':9999, 'desc':'Field 127.25 - Integrated circuit card (ICC) data'},
        26: {'data_format':'ans',    'len_format':'LL',    'max_len':20,   'desc':'Field 127.26 - Original Node'},
        27: {'data_format':'ans',    'len_format':'F',     'max_len':1,    'desc':'Field 127.27 - Card Verification Result'},
        28: {'data_format':'n',      'len_format':'F',     'max_len':4,    'desc':'Field 127.28 - American Express Card Identifier (CID)'},
        29: {'data_format':'b',      'len_format':'F',     'max_len':40,   'desc':'Field 127.29 - 3-D Secure Data'},
        30: {'data_format':'ans',    'len_format':'F',     'max_len':1,    'desc':'Field 127.30 - 3-D Secure Result'},
        31: {'data_format':'ans',    'len_format':'LL',    'max_len':11,   'desc':'Field 127.31 - Issuer Network Id'},
        32: {'data_format':'b',      'len_format':'LL',    'max_len':33,   'desc':'Field 127.32 - UCAF Data'},
        33: {'data_format':'n',      'len_format':'F',     'max_len':4,    'desc':'Field 127.33 - Extended Transaction Type'},
        34: {'data_format':'n',      'len_format':'F',     'max_len':2,    'desc':'Field 127.34 - Account Type Qualifiers'},
        35: {'data_format':'ans',    'len_format':'LL',    'max_len':11,   'desc':'Field 127.35 - Acquirer Network ID'},
        36: {'data_format':'ans',    'len_format':'LL',    'max_len':25,   'desc':'Field 127.36 - Customer ID'},
        37: {'data_format':'an',     'len_format':'F',     'max_len':4,    'desc':'Field 127.37 - Extended Response Code'},
        38: {'data_format':'an',     'len_format':'LL',    'max_len':99,   'desc':'Field 127.38 - Additional POS Data Code'},
        39: {'data_format':'an',     'len_format':'F',     'max_len':2,    'desc':'Field 127.39 - Original Response Code'},
        40: {'data_format':'ans',    'len_format':'LLL',   'max_len':512,  'desc':'Field 127.40 - Transaction Reference'},
        41: {'data_format':'ans',    'len_format':'LL',    'max_len':99,   'desc':'Field 127.41 - Originating Remote Address'},
        42: {'data_format':'n',      'len_format':'LL',    'max_len':10,   'desc':'Field 127.42 - Transaction Number'}
    }


class Sd(Field):
    ''' Structure data object for 127.22 field
    
    Create a Postilion structure data object and related operations
    
    Attributes:
        fields: a dict storing the sd key and value, it should be accessed with method provided.
        
        CODING: the coding of the sd, which is ascii.
        SD_LEN_DIGITS: the number of digits used for indicating sd length.     
    '''
    
    CODING = 'ascii'
    SD_LEN_DIGITS = 5
    
    def __init__(self, value=None):
        ''' Create a structure data object with optional value 
        
        Args: value is a optional for building the sd based on string value
        '''
        self.fields = {}
        super(Sd,self).__init__(value, 22, Private.field_def[22], self.CODING)
        if value is not None:
            self.from_msg(value)

    def set_tag(self,tag,value):
        ''' Set a tag in sd with value '''
        self.fields[tag] = value
            
    def get_tag(self,tag=None):
        ''' Get a tag in sd, return the full sd string if tag is None '''
        if tag is None:
            return self.to_msg()
        if tag not in self.fields.keys():
            return None
        else:
            return self.fields[tag]
    
    def clear_tag(self,tag):
        ''' Clear a tag in sd return if the tag not found '''
        if tag not in self.fields.keys():
            return
        else:
            del(self.fields[tag])
    
    def to_msg(self):
        ''' Return a bytearray for the whole sd with ASCII coding '''         
        result = bytearray(b'')
        if (len(self.fields.keys())) < 1:
            return result
        output_str = ''
        for key in sorted(self.fields.keys()):
            value = self.fields[key]
            len_key = len(key)
            len_len_key = len(str(len_key))
            len_value = len(value)
            len_len_value = len(str(len_value))
            
            output_str += str(len_len_key) + str(len_key) + key + str(len_len_value) + str(len_value) + value
            
        len_field = str(len(output_str))  
        result.extend(len_field.zfill(self.SD_LEN_DIGITS).encode(self.CODING))
        result.extend(output_str.encode(self.CODING))
        return result
    
    def from_msg(self, msg):
        ''' Parse message from string to sd object
         
        Args: msg containing a string of the whole sd field. 
        '''
        
        if msg is None: return
        p = 0
        #Parse __fields
        while True:
            len_len_key = int(msg[p:p+1])
            p += 1
            len_key = int(msg[p:p+len_len_key])
            p += len_len_key
            key = msg[p:p+len_key]
            p += len_key
            len_len_value = int(msg[p:p+1])
            p += 1
            len_value = int(msg[p:p+len_len_value])
            p += len_len_value
            value = msg[p:p+len_value]
            p += len_value
            self.fields[key] = value
            if p == len(msg): break
    
    def __str__(self):
        output = ''
        for key in sorted(self.fields.keys()):
            output += ' ' * 21 + "127.22.{}\n".format(key)
            output += ' ' * 26 + "[{}]\n".format(self.fields[key])
        return output
