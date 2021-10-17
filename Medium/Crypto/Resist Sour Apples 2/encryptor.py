import operator as op
from functools import reduce
from Crypto.Util.number import isPrime
import random

def nCr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom

#Returns the smallest prime >= x
def p(x):
    while not isPrime(x):
        x += 1
    return x

#Based on the Binomial Expansion of (ax+b)^c
def binom(a, b, c):
    n = 1
    for k in range(c+1):
        n *= p(nCr(c, k) * a**(c-k) * b**k)**(c-k)
    return n

def encode(s):
    v = 0
    for c in s:
        v *= 256
        v += ord(c)
    return v

def main():
    a = random.randint(10, 25)
    b = random.randint(10, 25)
    c = random.randint(10, 25)
    n = binom(a, b, c)
    e = 65537

    flag = open('flag.txt', 'r')
    pt = encode(flag.read())
    if(pt > n):
        print("Plaintext Error")
        return

    ct = pow(pt, e, n)

    f = open("enc", "w")
    f.write(f'a = {a}\n')
    f.write(f'b = {b}\n')
    f.write(f'c = {c}\n')
    f.write(f'n = {n}\n')
    f.write(f'e = {e}\n')
    f.write(f'ct = {ct}\n')

main()
