class Id:
    def __init__(self,id):
        self.digits = [id[0],id[1],id[2],id[3]]
        self.key = id[5]
    
    def is_digits_int(self):
        if (self.digits[0] == '?') or (self.digits[1] == '?') or (self.digits[2] == '?') or (self.digits[3] == '?'):
            return False
        else:
            self.digits[0] = int(self.digits[0])
            self.digits[1] = int(self.digits[1])
            self.digits[2] = int(self.digits[2])
            self.digits[3] = int(self.digits[3])
            return True
        
    def is_key_int(self):
        if (self.key == '?'):
            return False
        else:
            self.key = int(self.key)
            return True
        
    def find_key(self):
        if self.is_digits_int():
            total = 2*self.digits[0] + 3*self.digits[1] + 5*self.digits[2] + 7*self.digits[3]
            found_key = total%11
            return found_key
        else:
            print("A missing argument exist try .fill_digits")
        
    def check_valid(self):
        if self.is_digits_int() == True:
            found_key = self.find_key() 
            if found_key == int(self.key):
                print("VALID")
            else:
                print("INVALID")
        else:
            print("A missing argument exist try .fill_digits")
            
    def fill_key(self):
        self.key = self.find_key()
    
    def fill_digit(self):
        if self.is_key_int() == True:
            if self.digits[0] == '?':
                raw = -3*int(self.digits[1]) -5*int(self.digits[2]) -7*int(self.digits[3])
                raww = raw+int(self.key)
                while (raww<0) or not(raww%2==0):
                    raww = raww+11
                self.digits[0] = int(raww/2)

            elif self.digits[1] == '?':
                raw = -2*int(self.digits[0]) -5*int(self.digits[2]) -7*int(self.digits[3])
                raww = raw+int(self.key)
                while (raww<0) or not(raww%3==0):
                    raww = raww+11
                self.digits[1] = int(raww/3)

            elif self.digits[2] == '?':
                raw = -2*int(self.digits[0]) -3*int(self.digits[1]) -7*int(self.digits[3])
                raww = raw+int(self.key)
                while (raww<0) or not(raww%5==0):
                    raww = raww+11
                self.digits[2] = int(raww/5)

            elif self.digits[3] == '?':
                raw = -2*int(self.digits[0]) -3*int(self.digits[1]) -5*int(self.digits[2])
                raww = raw+int(self.key)
                while (raww<0) or not(raww%7==0):
                    raww = raww+11
                self.digits[3] = int(raww/7)
        else:
            print("A missing argument exist try .fill_key")
        
    def check_id(self):
        if self.is_digits_int() and self.is_key_int():
            self.check_valid()
        
        elif not(self.is_key_int()):
            self.fill_key()
            self.print_id()
        
        elif not(self.is_digits_int()):
            self.fill_digit()
            self.print_id()
            
            
    def print_id(self):
        id = str(self.digits[0])+str(self.digits[1])+str(self.digits[2])+str(self.digits[3])+"-"+str(self.key)
        print(id)
            
            
id = input("Input ver:")

id_object = Id(id)

id_object.check_id()
