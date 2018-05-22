import os
import sys
import socketserver
import threading
from pystilion.sdk.message import iso8583post
from pystilion.sdk.trace.trace import Trace
from pystilion.app.nidserver import configloader

class NidServerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        import filters
        trace = self.server.trace
        config = self.server.config
        entity_name = configloader.get_entity_name( str(self.client_address[0]), str(self.client_address[1]), config )
        trace.log("[{}] Client connected from {}".format(entity_name, str(self.client_address)))
        msg_len = -1
        received_data = bytearray()
        while True:
            data = None
            try:
                data = self.request.recv(1024).strip()
            except ConnectionResetError:
                trace.log("[{}] Client closed by remote with Reset {}".format(entity_name, str(self.client_address)))
            except Exception as ex:
                trace.log("[{}] ERROR: while receiving message from {}".format(entity_name, str(self.client_address)), None, None, ex)
            if not data:
                break
            received_data.extend(data)
            """Calculate the 2 bytes header"""
            if msg_len == -1 and len(received_data) >= 2:
                msg_len = received_data.pop(0) * 256 + received_data.pop(0)
            if msg_len == len(received_data):
                
                trace.log("[{}] Received data from {} Total length:{}".format(entity_name, str(self.client_address), str(msg_len)), str(msg_len), bytes(received_data))
                msg = iso8583post.Iso8583Post(bytes(received_data))
                trace.log("[{}] <{}> Message FROM {}".format(entity_name, msg.MTI, str(self.client_address)), str(msg), bytes(received_data))
                
                new_msg = None
                try:
                    new_msg = filters.update_msg(msg, trace, entity_name, config['CustomConfig'])
                except Exception as e:
                    trace.log("[{}] Exception while processing filters".format(entity_name), None, None, e)
                else:
                    trace.log("[{}] <{}> Message TO {}".format(entity_name, new_msg.MTI, str(self.client_address)), str(new_msg), bytes(new_msg.to_msg()))
        
                try:
                    if new_msg:
                        self.request.sendall(bytes(new_msg.to_msg()))
                except ConnectionResetError:
                    trace.log("[{}] Client closed by remote with Reset {}".format(entity_name, str(self.client_address)))
                except Exception as ex:
                    trace.log("[{}] ERROR: while sending message to {}".format(entity_name, str(self.client_address)), None, None, ex)                        
                
                """reset flag"""
                msg_len = -1
                received_data.clear()
                
    def setup(self):
        self.server.trace.log("Accepting client from {}".format( str(self.client_address) ))
        
    def finish(self):
        self.server.trace.log("Client closed {}".format( str(self.client_address) ))

class ThreadedNidServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def main():
    print ("INFO: Starting pyNid Server ...")
    
    if len(sys.argv) > 1: 
        config = configloader.load_config(sys.argv[1])
    else:
        config = configloader.load_config()
    
    trace_folder = config.get("Trace","TraceFolder")
    trace_header = config.get("Trace","HeaderTemplate")
    trace_trailer = config.get("Trace","TrailerTemplate")
    trace_maxSize = config.getint('Trace', 'FileSize')
    trace_maxFiles = config.getint('Trace', 'NumberOfFiles')
    trace = Trace(trace_folder, 'pyNidServer', trace_header, trace_trailer, trace_maxSize, trace_maxFiles)
    print ("INFO: Starting trace in " + trace_folder)
    
    module_folder = config.get("Process","ModuleFolder")
    sys.path.insert(0,module_folder)
    
    HOST = config.get("Connection","Hostname")
    PORT = config.getint("Connection","LocalPort")    
    print ("INFO: Starting server at {}:{}".format(HOST,str(PORT)))
    server = ThreadedNidServer((HOST, PORT), NidServerHandler)
    server.allow_reuse_address=True
    # pass the current_trace to server
    server.trace = trace
    # pass the config to server
    server.config = config    
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    IP, PORT = server.server_address
    print ("INFO: Server started at {}:{}".format(IP,str(PORT)))
    trace.log("-----------------------------------------------------------------------------------------------------")
    trace.log("Server started at {}:{}".format(IP,str(PORT)))
    server.serve_forever()
    
if __name__ == "__main__":
    main()