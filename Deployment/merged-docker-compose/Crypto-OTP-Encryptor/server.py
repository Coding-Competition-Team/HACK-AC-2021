#!/usr/local/bin/python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii

def randInt(a,b,c,d):
    return ((a-b)**2 + (c-d)**2 + (a+d)**2 + (b+c)**2)-(a*b*c*d)  

class PRNG:
    def __init__(self,seed0,seed1):
        self.seed0 = seed0;
        self.seed1 = seed1;
        self.L = 1;

    # Returns a random number
    def rand(self,a,b):
        return randInt(self.seed0, self.seed1, a, b)

flag = open('flag.txt','rb').read().decode("utf-8");
flag0 = flag[:len(flag) // 2];
flag1 = flag[len(flag) // 2:len(flag)];

def str2Dec(str):
    return int(binascii.hexlify(str.encode("utf-8")),16);

def Pad(msg):
    if (len(msg) <16):
        msg = pad(msg,16)
    elif (len(msg)>16):
        msg = msg[0:16]
    return msg

seed0 = str2Dec(flag0)
seed1 = str2Dec(flag1)
g = PRNG(seed0,seed1)

Welcome = "Welcome to the latest OTP encryptor and decryptor. Why bother trying to remember long annoying complicated OTP numbers when you can just remember two numbers :D"
print(Welcome);
options = "\nSelect an option:\nGenerate a new OTP (E)\nDecrypt an OTP     (D)\n"

while True:
    print(options)
    e_or_d = input()
    if("e" in e_or_d.lower()):
        try:
            print("Please enter your secret chosen password: ")
            iv = Pad(input().encode("utf-8"))
            print("Please enter your first number: ")
            a = int(input())
            print("Please enter your second number: ")
            b = int(input())
            number = str(g.rand(a,b)).encode("utf-8")
            key = Pad(number)
            cipher = AES.new(key, AES.MODE_OFB,iv=iv)
            OTP = cipher.encrypt(number)
            print("OTP Encrrypted Format: ",binascii.hexlify(OTP))
        except:
            print("Something went wrong, exiting now")
            exit()

    elif("d" in e_or_d.lower()):
        try:
            print("Please enter your secret chosen password: ")
            iv = Pad(input().encode("utf-8"))
            print("Please enter you OTP encrypted hex: ")
            otp = input()
            otp = binascii.unhexlify(otp)
            print("Please enter your first number: ")
            a = int(input())
            print("Please enter your second number: ")
            b = int(input())
            try:
                number = str(g.rand(a,b)).encode("utf-8")
                key = Pad(number)
                cipher = AES.new(key, AES.MODE_OFB,iv=iv)
                OTP = cipher.decrypt(otp)
                print("OPT Decrypted Format: ", OTP)
            except ValueError as KeyError:
                print("Something went awfully wrong today")
        except:
            print("something went wrong, exiting now")
            exit()

    else:
        print("sorry I didnt get that. Exiting now")
        exit()

        



