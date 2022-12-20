from flask import Flask, render_template
import time
from random import random
import random as rand
import copy
import math
app = Flask(__name__)
counter = 0


def RNG():
    global counter
    checker = 0.9
    value = random()
    counter += 1
    rounder = round(value, 1)
    if rounder == checker:
        auxi = counter
        counter = 0
        return [value, rounder, auxi, "Done"]
    return [value, rounder, counter, 0]



def reverse(n):
    inv = int(str(n)[::-1])
    return inv


def divisors_and_prime(n):
    nr = 0
    div = []
    for d in range(2, (n // 2) + 1):
        if n % d == 0:
            nr = nr + 1
            div.append(d)
    if nr == 0:
        isPrime = "Prime"
    else:
        isPrime = ""
    return [div, isPrime]


def digits_and_sumofdigits(n):
    S = set()
    sum = 0
    while n:
        sum = sum + n % 10
        x = n % 10
        n = n // 10
        S.add(x)
    return sum, S


def binary(n):
    c = copy.copy(n)
    bi = bin(c)[2:]
    return bi


def primeFactors(n):
    primes = []
    c = 2
    while n > 1:
        if n % c == 0:
            primes.append(c)
            n = n / c
        else:
            c = c + 1
    return primes


def Solutions(n):
    rev = reverse(n)
    Div_Prime = divisors_and_prime(n)
    div = Div_Prime[0]
    prime = Div_Prime[1]
    Sum_Digit = digits_and_sumofdigits(n)
    sum = Sum_Digit[0]
    digits = Sum_Digit[1]
    bi = binary(n)
    prime_fact = primeFactors(n)
    return [rev, div, prime, sum, digits, bi, prime_fact]




@app.route('/')
def Home():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return render_template('index.html', timenow=current_time)


@app.route('/RNG')
def RNJesus():
    Aux = RNG()
    return render_template('RNG.html', RNG=Aux[0], rounder=Aux[1], counter=Aux[2], Dummy=Aux[3])


@app.route('/All_in_1')
def All_in_1():
    n = rand.randint(0, 100)
    Aux = Solutions(n)
    return render_template('All_in_1.html', Nr=n, Rev=Aux[0], Div=Aux[1], Prime=Aux[2], Sum=Aux[3], Digits=Aux[4], Bi=Aux[5], PrimeFact=Aux[6])




if __name__ == '__main__':
    app.run()
