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
#    self.a2 = deque([0.0]*maxLen)
#    self.a3 = deque([0.0]*maxLen)
#    self.a4 = deque([0.0]*maxLen)
#    self.a5 = deque([0.0]*maxLen)
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
#    self.addToBuf(self.a2, data[2])
#    self.addToBuf(self.a3, data[3])
#    self.addToBuf(self.a4, data[4])
#    self.addToBuf(self.a5, data[5])
    
# plot class
class AnalogPlot:
  # constr
  def __init__(self, analogData):
    # set plot to animated
    plt.ion() 
    self.a0line, = plt.plot(analogData.a0)
    self.a1line, = plt.plot(analogData.a1)
#    self.a2line, = plt.plot(analogData.a2)
#    self.a3line, = plt.plot(analogData.a3)
#    self.a4line, = plt.plot(analogData.a4)
#    self.a5line, = plt.plot(analogData.a5)
    plt.ylim([-2,2])
 
  # update plot
  def update(self, analogData):
    self.a0line.set_ydata(analogData.a0)
    self.a1line.set_ydata(analogData.a1)
#    self.a2line.set_ydata(analogData.a2)
#    self.a3line.set_ydata(analogData.a3)
#    self.a4line.set_ydata(analogData.a4)
#    self.a5line.set_ydata(analogData.a5)
    plt.pause(0.01)
 
# main() function
def main():
  # expects 1 arg - serial port string
  if(len(sys.argv) != 2):
    print ('Example usage: python showdata.py "/dev/tty.usbmodem411"')
    exit(1)
 
 #strPort = '/dev/tty.usbserial-A7006Yqh'
  strPort = sys.argv[1];
 
  # plot parameters
  analogData = AnalogData(100)
  analogPlot = AnalogPlot(analogData)
 
  print ('plotting data...')
 
  # open serial port
  ser = serial.Serial(strPort, 9600)
  f=open("temp.csv","w+")
  while True:
    try:
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
        analogData.add(data2)
        analogPlot.update(analogData)
    except KeyboardInterrupt:
      print ('exiting')
      break
  # close serial
  f.close()
  ser.flush()
  ser.close()
 
# call main
if __name__ == '__main__':
  main()
