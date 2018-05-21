import os
import traceback
import configparser
from pystilion.app.nidserver import error


def load_config(config_filename=None):
    if not config_filename:
        print ("INFO: Config File not specified, use default location")
        cwd = os.getcwd()
        config_filename = os.path.join(cwd,'config','config.ini')
    print ("INFO: Loading Config File from {}".format(config_filename))
    config = configparser.ConfigParser()
    try:
        config.read(config_filename)
        validate_config(config)
    except Exception as e:
        print (e)
        traceback.print_exc()
        exit(1)
    return config

def validate_config(config):
    
    # define mandate config - None or config with default fallback
    default_parm = {
        'Trace' : { 
            'TraceFolder' :     '.\\trace',
            'HeaderTemplate' :  None,
            'TrailerTemplate' : None,
            'FileSize'        : '5',
            'NumberOfFiles'   : '5',
        },
        'Connection' : {
            'Hostname' :        '0,0,0,0',
            'LocalPort' :       '9999',
        },
        'Process' : {
            'ModuleFolder' :    '.\\config',
        },
        'EntityMapping' : {
            '* *' :             'unknown',
        },
        'CustomConfig' : {
        },
    }
    
    # check mandate sections / fields
    for s in default_parm.keys():
        for p in default_parm[s].keys():
            # if parm located in the file
            if s in config.keys() and p in config[s]:  
                continue
            # add default section and parameter if parm not located
            elif  default_parm[s][p] != None:
                if not config.has_section(s):
                    print("INFO: Section {} added for default parameter {}".format(s,p))
                    config.add_section(s)
                config[s][p] = default_parm[s][p]
                print("INFO: Default parameter {} added with value {}".format(p,default_parm[s][p]))
            # Mandate section not presented in file and no default defined
            elif  default_parm[s][p] == None and s not in config:
                raise error.configError("Section {} is not defined in config file".format(s))
            # Mandate parm not presented in file and no default defined
            elif  default_parm[s][p] == None and s not in config[s]:
                raise error.configError("Parameter {} in section {} is not defined in config file".format(p,s))
    
    # check logic config values
    try: 
        p = config.getint('Trace', 'FileSize')
    except Exception:
        raise error.configError("Config Trace/FileSize must be an int")
    else:
        if p < 1:
            raise error.configError("Config Trace/FileSize must be an int >= 1")
    
    try: 
        p = config.getint('Trace', 'NumberOfFiles')
    except Exception:
        raise error.configError("Config Trace/NumberOfFiles must be an int")
    else:
        if p < 1:
            raise error.configError("Config Trace/NumberOfFiles must be an int >= 1")
        
    try: 
        p = config.getint('Connection', 'LocalPort')
    except Exception:
        raise error.configError("Config Connection/LocalPort must be an int")
    else:
        if p < 1 or p > 65535:
            raise error.configError("Config Connection/LocalPort must be an int >= 1 and <= 65535")

def get_entity_name(ip, port, config):
    for i in config['EntityMapping']:
        if ip == i.split()[0] and port == i.split()[1]:
            return config['EntityMapping'][i]
    for i in config['EntityMapping']:
        if i.split()[0] == '*' and port == i.split()[1]:
            return config['EntityMapping'][i]
    for i in config['EntityMapping']:
        if ip == i.split()[0] and i.split()[1] == '*':
            return config['EntityMapping'][i]    
    return 'unknown'

if __name__ == "__main__":
    config = load_config()
    print (get_entity_name('1.1.1.1', '20002', config))