from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

KEY = os.urandom(16)

class Counter(object):
    def __init__(self, value = os.urandom(16).hex(), decrease = True):
        self.value = value
        self.step = 1
        self.step_up = not decrease

    def increment(self):
        if self.step_up:
            self.newIV = hex(int(self.value, 16) + self.step)
        else:
            self.newIV = hex(int(self.value, 16) - self.step)
        self.value = self.newIV[2:len(self.newIV)]
        self.__init__(self.value, self.step_up)
        return bytes.fromhex(self.value.zfill(32))

def encrypt():
    cipher = AES.new(KEY, AES.MODE_ECB)
    ctr = Counter()

    out = open("enc", "w")
    with open("flag.png", 'rb') as f:
        block = f.read(8)
        while block:
            block = pad(block, 16)
            keystream = cipher.encrypt(ctr.increment())
            xored = [a^b for a, b in zip(block, keystream)]
            out.write(bytes(xored).hex())
            block = f.read(8)

encrypt()