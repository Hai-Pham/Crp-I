
from gmpy2 import isqrt, isqrt_rem, sub, add, mul, mpz, div, powmod, invert
from binascii import unhexlify
import math


class bad_rsa:
    def __init__(self, N):
        self.N = N
        self.computePrime()

    def computePrime(self):
        for i in range(1, 2**20):
            self.A = isqrt(self.N) + i
            self.calcX()
            if self.verify():
                print(i)
                print("found it!")
                print(self.p)
                break

    def calcX(self):
        Asquared = mul(self.A, self.A)
        remainder = sub(Asquared, self.N)
        self.x  = isqrt_rem(remainder)[0]

    def verify(self):
        self.p = sub(self.A, self.x)
        self.q = add(self.A ,self.x)
        if mul(self.p, self.q) == self.N:
            return True
        else:
            return False

# a = bad_rsa(prob1)



#problem 1
prob1 = mpz('17976931348623159077293051907890247336179769789423065727343008115' +
                   '77326758055056206869853794492129829595855013875371640157101398586' +
                   '47833778606925583497541085196591615128057575940752635007475935288' +
                   '71082364994994077189561705436114947486504671101510156394068052754' +
                   '0071584560878577663743040086340742855278549092581')

prob2 = mpz('6484558428080716696628242653467722787263437207069762630604390703787' +
                  '9730861808111646271401527606141756919558732184025452065542490671989' +
                  '2428844841839353281972988531310511738648965962582821502504990264452' +
                  '1008852816733037111422964210278402893076574586452336833570778346897' +
                  '15838646088239640236866252211790085787877')
prob3 = mpz('72006226374735042527956443552558373833808445147399984182665305798191' +
                '63556901883377904234086641876639384851752649940178970835240791356868' +
                '77441155132015188279331812309091996246361896836573643119174094961348' +
                '52463970788523879939683923036467667022162701835329944324119217381272' +
                '9276147530748597302192751375739387929')
e = 65537
c = mpz('22096451867410381776306561134883418017410069787892831071731839143676135600120538004282329650473509424343946219751512256465839967942889460764542040581564748988013734864120452325229320176487916666402997509188729971690526083222067771600019329260870009579993724077458967773697817571267229951148662959627934791540')

#Problem 1 and 2
def factorN(prob):
    AA = isqrt(prob)
    for i in range(1, 2**20):
        A = AA + i
        x = isqrt_rem(mpz(A**2 -prob))[0]
        assert x > 0
        p = mpz(A - x)
        q = mpz(A + x)
        print(i)
        if mul(p,q) == prob:
            print("FOUND IT")
            print(p)
            return (p,q)
            break

    # let M = (3p+2q)/2
    # M is not an integer since 3p + 2q is odd
    # So there is some integer A = M + 0.5 and some integer i such that
    # 3p = M + i - 0.5 = A + i - 1 => p = (A + i - 1)/2
    # and
    # 2q = M - i + 0.5 = A - i => q = (A-i)/2
    #
    # N = pq = (A-i)(A+i-1)/6 = (A^2 - i^2 - A + i)/6
    # So 6N = A^2 - i^2 - A + i
    # i^2 - i = A^2 - A - 6N
def factorN3(prob):
    print("start challenge 3")
    AA,r = isqrt_rem(6*prob)
    A = AA + (1 if r else 0)

    # Solve i^2 - i = A^2 - A - 6N
    # as ax^2 - bx + c = 0
    a = mpz(1)
    b = mpz(-1)
    c = -(A**2 - A - 6*prob)

    roots = (
        div(-b + isqrt(b**2 - 4*a*c), 2*a),
        div(-b - isqrt(b**2 - 4*a*c), 2*a)
    )

    for x in roots:
        if x >= 0:
            p = div(A + x -1, 3)
            q = div(A - x, 2)
            isCorrect = (p*q == prob)
            if isCorrect:
                print("OK")
                print(p if p < q else q)
                return p if p < q else q
            else:
                p = div(A + x -1, 2)
                q = div(A - x, 3)
                isCorrect = (p*q == prob)
                if isCorrect:
                    print("OK2")
                    print(p if p < q else q)
                    return p if p < q else q

#end of factor3


def decRSA(ciphertext, N, e):
    #pk = (N,e)
    (p,q) = factorN(prob1)

    phi = N - p - q + 1

    #sk = d: de = -1 (mod phi)
    d = invert(e, phi)

    plaintext = hex(powmod(ciphertext, d, N))
    print(plaintext)

    return plaintext


print("Challenge 2")
factorN(prob2)
print("Challenge 3")
factorN3(prob3)
print("Challenge 1")
factorN(prob1)

print("decrypt RSA")
pkcs1 = decRSA(c, prob1, e)
i = pkcs1.find("00")
text = unhexlify(pkcs1[pkcs1.find("00")+2:]).decode()
print(text)