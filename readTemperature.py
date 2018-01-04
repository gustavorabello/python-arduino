## =================================================================== ##
#  this is file readTemperatureHumidity.py, created at 03-Jan-2018      #
#  maintained by Gustavo Rabello dos Anjos                              #
#  e-mail: gustavo.rabello@gmail.com                                    #
## =================================================================== ##

import serial
from serial.tools import list_ports
import matplotlib.pyplot as plt

selectedPortIndex = 1;
selectedDevice = "";
ports = list_ports.comports();

# print available ports
#print("Avaiable ports:\n%s"%"\n".join(["\t%d: %s"% (portIndex,str(ports[portIndex])) for portIndex in range(len(ports))]))

selectedDevice = ports[selectedPortIndex].device
print("Selected device: %s"%selectedDevice)

# select device port
ser = serial.Serial(selectedDevice, 9600)

timeCount = 0
timeHist = []
tempAnalHist = []
for line in ser:
 entry = line.decode("utf-8").split("\t")
 tempAnal = entry[0]
 tempAnal = float(tempAnal.split()[1])
 humidity = entry[1]
 humidity = float(humidity.split()[1])
 tempDig = entry[2]
 tempDig = float(tempDig.split()[1])
 time = entry[3]
 time = float(time.split()[1])
 timeCount += time/1000
 
 # single plot
 #print tempAnal,humidity,tempDig
 #plt.plot(timeCount,tempAnal,'bo')
 #plt.axis([0.0,300.0,22,35])

 # data history and plot with line
 timeHist.append(timeCount)
 tempAnalHist.append(tempAnal)
 plt.plot(timeHist,tempAnalHist,'b-')
 plt.plot(timeHist,humidityHist,'r-')
 plt.axis([min(timeHist)*0.9,
           max(timeHist)*1.1,
           min(tempAnalHist)*0.9,
           max(tempAnalHist)*1.1])

 plt.xlabel('time[s]')
 plt.ylabel('temperature[*C]')
 #file = 'colision' + str(i) + '.png'
 #plt.savefig(file)
 #plt.close()
 plt.pause(timeCount)
 print timeCount
 #plt.clf()

