from winreg import *

class Registry(object):
    def __init__(self):
        self.back_up = {}
        
    def write(self, path, values):
        with OpenKey(HKEY_LOCAL_MACHINE, path, 0, KEY_ALL_ACCESS) as key:
            for name, value in values.items():
                print name, value
                SetValueEx(key, name, 0, REG_SZ, value)
                
                
def main():
    reg = Registry()
    reg.write(r'SOFTWARE\\Python', {"(Default)":'1'})
    
main()
            