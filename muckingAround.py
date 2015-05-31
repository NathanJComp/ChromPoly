__author__ = 'Nathan'
from sympy import Symbol
from sympy import div
import sympy

x = Symbol('x')
def Poly(p,mod):
    q,r = div(p,mod,x) #quotient and remainder polynomial division by modulus mod
    return r.as_poly(x,domain='GF(2)') #Z_2

m = x**8 + x**4 + x**3 + x + 1
p = x**6 + x**5 + x + 1


a=x**2+2*x+2
b=3*x**6+2*x**5-69*x**4+148*x**3-84*x**2

#returns the degree of the largest complete polynomial which divids poly
def hasComplete(poly):
    divides=True
    order=0
    while(divides):
        q,r=div(poly,x-order)
        if r!=0:
            divides=False
        else:
            order+=1
    return order
print(hasComplete(b))