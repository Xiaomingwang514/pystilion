from pystilion.sdk.trace.trace import Trace
import os

if __name__ == "__main__":
    print(os.getcwd())
    trace = Trace('../../../trace', 'pyNidServer', '../../../config/trace_header.ht_', '../../../config/trace_trailer.ht_')
    trace.log("aaaa<>a")
    trace.log("accc", "bbbb<b")
    trace.log("ac'c", "bbbbbb", b'\x38\x32\x36\x38\x32\x36\x38\x32\x36\x38\x32\x36\x38\x32\x36\x38\x32\x36')
    trace.log("accc", "bbbbb>b", b'\x80\x32\x36',"ddddddddddddd")
