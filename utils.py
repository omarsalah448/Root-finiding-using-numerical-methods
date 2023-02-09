# VIP, if any of the libraries used here not installed for you
# then open cmd and type "pip install <library name>"
import re
import math
import sympy as sym
from tkinter import *

def parser(eqn, x=0):
    # handle exponential
    eqn=re.sub(r"(e)(\^|\*\*)(x|-x)", r"exp(\3)", eqn)
    # handle polynomial
    eqn=re.sub(r"(sin|cos|tan|exp)", r"math.\1", eqn)
    # handle power case
    eqn=re.sub("\^","**", eqn)
    # handle digits
    eqn=re.sub(r"([0-9])([^+-.*[0-9]])", r"\1*\2", eqn)
    eqn=re.sub(r"([0-9])(x)", r"\1*\2", eqn)
    # handle log(e)
    eqn=re.sub("log\(e\)", "1", eqn)
    # handle y= case
    eqn=re.sub(".* =|.=", "", eqn)
    return eval(eqn)

def bisection(eqn, xl, xu, es=0.00001, iter_max=50):
    no_iter = 0
    ea = 100
    singleStepArray = [("Iter", "XL", "XU", "XR", "Ea")]
    if parser(eqn, xl)*parser(eqn, xu) > 0:
        return ("roots don't bracket :( ", 0, 0, [])
    for i in range(iter_max):
        xr = (xl+xu) / 2
        # to avoid division by 0
        if xr != 0 and no_iter > 0:
            ea = abs(xr-x_old) / xr
        x_old = xr
        val = parser(eqn, xl) * parser(eqn, xr)
        if val < 0:
            xu = xr
        else:
            xl = xr
        no_iter += 1
        singleStepArray.append((no_iter, xl, xu, xr, ea))
        if val == 0:
            ea = 0
            return (xr, ea, no_iter, singleStepArray)
        elif abs(ea) <= es:
            return (xr, ea, no_iter, singleStepArray)
    return (xr, ea, no_iter, singleStepArray)

def falsePosition(eqn, xl, xu, es=0.00001, iter_max=50):
    no_iter = 0
    ea = 100
    ya = parser(eqn, xl)
    yb = parser(eqn, xu)
    singleStepArray = [("Iter", "XL", "XU", "f(XL)", "f(XU)", "XR", "Ea")]
    if ya*yb > 0:
        return ("roots don't bracket :( ", 0, 0, [])
    for i in range(iter_max):
        x = xu - ((xu-xl) * yb) / (yb-ya)
        y = parser(eqn, x)
        if x != 0 and no_iter > 0:
            ea = (x-x_old) / x
        x_old = x
        no_iter += 1
        singleStepArray.append((no_iter, xl, xu, ya, yb, x, ea))
        if y == 0:
            return (x, ea, no_iter, singleStepArray)
        elif y*ya < 0:
            xu = x
            yb = y
        else:
            xl = x
            ya = y
        if abs(ea) <= es:
            return (x, ea, no_iter, singleStepArray)
    return (x, ea, no_iter, singleStepArray)

def fixedPoint(eqn, xr, es=0.00001, iter_max=50):
    no_iter = 0
    ea = 100
    singleStepArray = [("Iter", "X OLD", "XR", "Ea")]
    x = sym.Symbol('x')
    derivative = sym.diff(eqn, x)
    val = parser(str(derivative), xr)
    if abs(val) >= 1:
        return ("this magic function won't converge :( ", 0, 0, [])
    for i in range(iter_max):
        x_old = xr
        xr = parser(eqn, x_old)
        singleStepArray.append((no_iter, x_old, xr, ea))
        if xr != 0 and no_iter > 0:
            ea = abs(xr-x_old) / xr
        no_iter += 1
        if abs(ea) <= es:
            return (xr, ea, no_iter, singleStepArray)
    return (xr, ea, no_iter, singleStepArray)

def newtonRaphson(eqn, xr, es=0.00001, iter_max=50):
    no_iter = 0
    ea = 100
    singleStepArray = [("Iter", "X OLD", "XR", "Ea")]
    for i in range(iter_max):
        x_old = xr
        x = sym.Symbol('x')
        derivative = sym.diff(eqn, x)
        xr = x_old - (parser(eqn, x_old)/parser(str(derivative), x_old))
        singleStepArray.append((no_iter, x_old, xr, ea))
        if xr != 0 and no_iter > 0:
            ea = abs(xr-x_old) / xr
        no_iter += 1
        if abs(ea) <= es:
            return (xr, ea, no_iter, singleStepArray)
    return (xr, ea, no_iter, singleStepArray)   

def secant(eqn, xl, xu, es=0.00001, iter_max=50):
    no_iter = 0
    ea = 100
    singleStepArray = [("Iter", "XL", "XU", "XR", "Ea")]
    for i in range(iter_max):
        xr = xu - (parser(eqn, xu)*(xu-xl) / (parser(eqn, xu)-parser(eqn, xl)))
        singleStepArray.append((no_iter, xl, xu, xr, ea))
        xl = xu
        xu = xr
        ea = abs(xu-xl) / xu
        no_iter += 1
        if abs(ea) <= es:
            return (xu, ea, no_iter, singleStepArray)
    return (xu, ea, no_iter, singleStepArray)   