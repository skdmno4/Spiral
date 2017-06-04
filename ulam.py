# -*- coding: utf-8 -*-
"""
@author: skmno4
Copyright (c) 2017 skmno4

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import numpy as np
import sys

class Q:
    """ state in spiral generation """
    def __init__(self, M, N):
        self.Active = "y"
        self.DelX = 0
        self.DelY = 1
        self.Xincr = 0
        self.Yincr = 1
        self.Direction = 1
        self.x = M//2
        self.y = N//2
        self.Val = 1
    def __repr__(self):
        return "Qi Active: %s, Del: [%s, %s], Incr: [%s, %s], Di: %s, point [%s,%s]"\
    " Val: %s" % (self.Active, self.DelX, self.DelY, self.Xincr, self.Yincr,\
                  self.Direction, self.x, self.y, self.Val)

class fullprint:
    'context manager for printing full numpy arrays'
    """https://stackoverflow.com/questions/1987694/print-the-full-numpy-array/1988024"""
    def __init__(self, **kwargs):
        if 'threshold' not in kwargs:
            kwargs['threshold'] = np.nan
        self.opt = kwargs

    def __enter__(self):
        self._opt = np.get_printoptions()
        np.set_printoptions(**self.opt)

    def __exit__(self, type, value, traceback):
        np.set_printoptions(**self._opt)

def AlignToLeastGreaterSquareRoot(num):
    if num == 1:
        return num
    else:
        for i in range(2, num//2):
            if i**2 >= num:
                return i
    return -1            
"""
State:
    Qi:Active, DelX, DelY, Xincr, Yincr, Direction, x, y, Val
    Active = x or y
    Xincr or Yincr = working length of current side of spiral
    Direction = 1 or -1 depending on up/right or down/left
    x, y current coordinate
    Val = value
    Q0: "y", 0, 1, 0, 1, 1, M/2, N/2, 1
    Q1: "x", 1, 0, 1, 1, 1, M/2, N/2+1, 2
    .
    .
    Qt:{
        if Qt-1:Active == "y"
            Qt:DelY = Qt-1:DelY - 1
            if !Qt:DelY
                Qt:Xincr:Qt:DelX = Qt-1:Xincr + 1
                Qt:Active="x"
            Qt:y = Qt-1:y + Qt-1:Direction
        if Qt-1:Active == "x"
            Qt:DelX = Qt-1:DelX - 1
            if !Qt:DelX
                Qt:Yincr:Qt:DelY = Qt-1:Yincr + 1
                Qt:Active = "y"
                Qt:Direction: -1 if Qt:Yincr & 1 else 1
            Qt:x = Qt-1:x + Qt-1:Direction
      if (Qt:x < M and Qt:y < N)
          Qt:Val = Qt-1:Val + 1
      else
          Qf = Qt
          return
    }
"""
old_stdout = sys.stdout
logFile = open("message.log","w")
sys.stdout = logFile
Mo=21    
No=21
#np.set_printoptions(threshold='nan')
def EndNotes(ulamSpi, m, n):
    print("evaluated spiral: ")
    with fullprint():
        print (ulamSpi)

M = N = AlignToLeastGreaterSquareRoot(Mo*No)

UlamSpi = np.zeros((M+1,N+1))
print(UlamSpi)
Q0 = Q(M, N)
Qprev = Q0
UlamSpi[M//2][N//2] = 1
Qcur = None
Qf = None
loopCtr = 0

#print(repr(Q0))
while Qf is None:
    """ find Qi """
    if loopCtr == Mo*No - 1:
        print("loop ran more than M*N ", loopCtr, " times")
        break
    loopCtr = loopCtr + 1
    if Qprev.x == M+1 or Qprev.y == N+1:
        Qf = Qprev
        print("Matrix is full. Break")
        break
    Qcur = Q0
    Qcur.Val = Qprev.Val + 1
    if Qprev.Active == "y":
        Qcur.DelY = Qprev.DelY - 1
        Qcur.x = Qprev.x
        Qcur.y = Qprev.y + Qprev.Direction        
        if 0 == Qcur.DelY:
            Qcur.DelX = Qcur.Xincr = Qprev.Xincr + 1
            Qcur.Active = "x"
    elif Qprev.Active == "x":
        Qcur.DelX = Qprev.DelX - 1
        Qcur.y = Qprev.y
        Qcur.x = Qprev.x + Qprev.Direction
        if Qcur.DelX == 0:
            Qcur.DelY = Qcur.Yincr = Qprev.Yincr + 1
            Qcur.Active = "y"
            Qcur.Direction = 1 if Qprev.Yincr & 1 == 1 else -1 
    #print(repr(Qcur))
    UlamSpi[Qcur.x][Qcur.y] = Qcur.Val
    Qprev = Qcur

EndNotes(UlamSpi, M, N)
sys.stdout = sys.__stdout__
logFile.close()

