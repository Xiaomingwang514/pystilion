#!/usr/bin/python3

import copy

def update_msg(msg, trace, entity_name, config):
    new_msg=copy.deepcopy(msg)
    
    return new_msg
        
    '''
	tracing - call trace.log(summary, detail, bytes, exception)
	config is a dict containing all items in [CustomConfig] section of config file
	entity_name can be used to identify the origin of the transation, but it need to be mapped in the config file.
	
    get incoming message MTI 
        msg.MTI
    set outgoing message MTI 
        new_msg.MTI = "0110"
    
    get basic field 
        msg.get_field(2)
    set basic field 
        new_msg.set_field(2,"1234123412341234")
    clear basic field 
        new_msg.clear_field(2)
    
    get private field 
        msg.private.get_field(2)
    set private field 
        new_msg.private.set_field(2,"1234123412341234")
    clear private field 
        new_msg.private.clear_field(2) 
    
    get sd tag 
        msg.private.sd.get_tag("aaa")
    set sd tag 
        new_msg.private.sd.get_tag("aaa","bbb")
    clear sd tag 
        new_msg.private.sd.clear_tag.("aaa") 
    
    check source of transaction 
        msg.private.sd.get_tag("PYNID_NAME") == "Apacs30Sink"
		if the entity mapping is setup, use entity_name is easier
		
    check the direction of transaction 
        msg.private.sd.get_tag("PYNID_DIRECTION") == "FROM_TM"
        msg.private.sd.get_tag("PYNID_DIRECTION") == "FROM_REMOTE"
    override the action 
        new_msg.private.sd.set_tag("PYNID_ACTION", "TO_TM" )
        new_msg.private.sd.set_tag("PYNID_ACTION", "TO_REMOTE" )
    '''    
        

    