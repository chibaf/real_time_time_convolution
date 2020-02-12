################################################################################
# showdata.py
#
# Display analog data from Arduino using Python (matplotlib)
# 
# electronut.in
#
################################################################################
 
import sys, serial
import numpy as np
from time import sleep
from collections import deque
from matplotlib import pyplot as plt
 
# class that holds analog data for N samples
class AnalogData:
  # constr
  def __init__(self, maxLen):
    self.a0 = deque([0.0]*maxLen)
    self.a1 = deque([0.0]*maxLen)
    self.maxLen = maxLen
 
  # ring buffer
  def addToBuf(self, buf, val):
    if len(buf) < self.maxLen:
      buf.append(val)
    else:
      buf.pop()
      buf.appendleft(val)
 
  # add data
  def add(self, data):
    assert(len(data) == 2)
    self.addToBuf(self.a0, (data[0]))
    self.addToBuf(self.a1, data[1])
#    self.addToBuf(self.a5, data[5])
    
# plot class
class AnalogPlot:
  # constr
  def __init__(self, analogData):
    # set plot to animated
    plt.ion() 
    self.a0line, = plt.plot(analogData.a0)
    self.a1line, = plt.plot(analogData.a1)
    plt.ylim([-2,2])
 
  # update plot
  def update(self, analogData):
    self.a0line.set_ydata(analogData.a0)
    self.a1line.set_ydata(analogData.a1)
    plt.pause(0.01)

def DotProduct(x,y):  # inner product
  r=0
  for i in range(0,len(x)):
    r=r+x[i]*y[i]
  return r

def findlm(x):
  for i in range(0,len(x)-1):
    j=0
    if (x[i]>x[i+1]):
      j=i
      break
  return j


# main() function
def main():
  # expects 1 arg - serial port string
  if(len(sys.argv) != 2):
    print ('Example usage: python showdata.py "/dev/tty.usbmodem411"')
    exit(1)
 
 #strPort = '/dev/tty.usbserial-A7006Yqh'
  strPort = sys.argv[1];
 
  # plot parameters
#  analogData = AnalogData(100)
#  analogPlot = AnalogPlot(analogData)
 
  print ('plotting data...')
 
  tc1 = [0] * 100
  tc2 = [0] * 100
  appnd  = [0] * 100
  cnv = [0]*100
  t=np.linspace(0.0,10.0,100)
  # open serial port
  ser = serial.Serial(strPort, 115200) # M5Stack Serial Speed
  f=open("temp1.csv","w+")
  g=open("temp2.csv","w+")
  i=0
  while True:
    try:
      if (i<100):
        line = ser.readline()
        data = [float(val) for val in line.split()]
        #print data
        if(len(data) == 3):
          print(data)
          flag=0
          for val in data:
            flag+=1
            f.write(str(val)); 
            if(flag<3): 
              f.write(", ")
          f.write("\n")
          flag=0
          data2=list([data[1],data[2]])
#          analogData.add(data2)
#          analogPlot.update(analogData)
        tc1[i]=data[1];tc2[i]=data[2];
        i=i+1
      elif (i<200):
#        analogData = AnalogData(100)
#        analogPlot = AnalogPlot(analogData)
        line = ser.readline()
        data = [float(val) for val in line.split()]
        #print data
        if(len(data) == 3):
          print(data)
          flag=0
          for val in data:
            flag+=1
            f.write(str(val)); 
            if(flag<3): 
              f.write(", ")
          f.write("\n")
          flag=0
          data2=list([data[1],data[2]])
#          analogData.add(data2)
#          analogPlot.update(analogData)
        appnd[i-100]=data[2];
        i=i+1
      else:
        for j in range(100):
          tc2.pop(0)
          tc2.insert(0,appnd[j])
          cnv[j]=DotProduct(tc1,tc2)
        i=0;
        plt.plot(t,cnv)
        plt.pause(0.1)
        lm=findlm(cnv)
        print(lm)
        g.write(str(lm));g.write("\n")
         
    except KeyboardInterrupt:
      print ('exiting')
      break
  # close serial
  f.close()
  g.close()
  ser.flush()
  ser.close()
 
# call main
if __name__ == '__main__':
  main()
