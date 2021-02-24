#Author      : Ramazan AKTAS
#Date        : 17.02.2021 22:00

from threading import Lock
import time

class lockable(object):
    """lockable variable class"""
    value = None
    lock = None

    def __init__(self, val):
        self.lock = Lock()
        self.value = val

    def SetValue(self, _value, key = None):
        
        #print("Lock will be acquired to SET VALUE\n")
        self.lock.acquire()
        try:
            if key is not None:
                if key in self.value:
                    self.value[key] = _value
                else:
                    print("Key is not implemented in dict: ", self.value)
            else:
                self.value = _value
        finally:
            self.lock.release()      
            #print("Lock will be released to SET VALUE\n")

    def GetValue(self, key = None):
        
        _value = None
        
        #print("Lock will be acquired to GET VALUE\n")
        self.lock.acquire()
        try:
            if key is not None:
                _value = self.value[key]
            else:
                _value = self.value
        finally:
            self.lock.release()      
            #print("Lock will be released to GET VALUE\n")
        
        return _value