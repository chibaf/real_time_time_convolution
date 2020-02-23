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
import re
 
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

def RotateLeft(x,n):  # n <= len(x)
  r=[]
  for i in range(0,len(x)):
    if i+n<len(x):
      r.append(x[i+n])
    else:
      r.append(x[i+n-len(x)])
  return r


# main() function
def main():
  # expects 1 arg - serial port string
  if(len(sys.argv) != 5):
    print ('Example usage: python showdata.py "/dev/tty.usbmodem411"')
    exit(1)
 
 #strPort = '/dev/tty.usbserial-A7006Yqh'
  strPort1 = sys.argv[1];
  strPort2 = sys.argv[2];
  file1=sys.argv[3];
  file2=sys.argv[4];
#  file3=sys.argv[5];
 
  # plot parameters
#  analogData = AnalogData(100)
#  analogPlot = AnalogPlot(analogData)
 
  print ('plotting data...')
 
  tc1 = [0] * 100
  tc2 = [0] * 100
  cnv = [0]*100
  t=np.linspace(0.0,10.0,100)
  # open serial port
  ser1 = serial.Serial(strPort1, 115200) # M5Stack Serial Speed
  ser2 = serial.Serial(strPort2, 9600) # Arduino Serial Speed
  f=open(file1,"w+")
  g=open(file2,"w+")
#  h=open(file3,"w+")
  i=0
  while True:
    data=[]
    try:
      for i in range(0,100):
        data=[]
        regex = re.compile('\d+')
        line = ser1.readline()
        word = ser2.readline()
#        print(line);print(word)
        try:
          match = regex.findall(str(line))
          data.append(float(match[1])*60.0+float(match[2])+float(match[3])*0.1)
          data.append(float(match[4]+"."+match[5]))
          data.append(float(match[6]+"."+match[7]))
          data.append(float(match[8]+"."+match[9]))
          data.append(float(match[10]+"."+match[11]))
          data.append(float(match[12]+"."+match[13]))
          data.append(float(match[14]+"."+match[15]))
          data.append(float(match[16]+"."+match[17]))
          data.append(float(match[18]+"."+match[19]))
          data.append(float(match[20]+"."+match[21]))
          data.append(float(match[22]+"."+match[23]))
          data.append(int(word))
        except:
          print(line);print(word)
          exit()
        print(data)
#        data1=[data[0],data[1],data[2]]
#        print(data1)
        #if(len(data) == 11):
        flag=0
        for val in data:
          flag+=1
          f.write(str(val)); 
          if(flag<12): 
            f.write(", ")
        f.write("\n")
#        h.write(str(word));
#        h.write("\n")
        flag=0
        data2=list([data[1],data[2]])
        tc1[i]=data[7];tc2[i]=data[8];
      cnv=[]
      for j in range(0,len(tc2)):
        cnv.append(DotProduct(tc1,RotateLeft(tc2,j)))
      plt.plot(t,cnv)
      plt.pause(0.1)
      lm=findlm(cnv)*0.1
      print(lm)
      g.write(str(lm))
      g.write("\n")
        
    except KeyboardInterrupt:
      print ('exiting')
      break
  # close serial
  f.close()
  g.close()
#  h.close()
  ser1.flush()
  ser1.close()
  ser2.flush()
  ser2.close()
 
# call main
if __name__ == '__main__':
  main()
