## =================================================================== ##
#  this is file readTemperatureHumidity.py, created at 03-Jan-2018      #
#  maintained by Gustavo Rabello dos Anjos                              #
#  e-mail: gustavo.rabello@gmail.com                                    #
## =================================================================== ##

import serial
from serial.tools import list_ports
import matplotlib.pyplot as plt
import numpy as np

selectedPortIndex = 1;
selectedDevice = "";
ports = list_ports.comports();
plt.ion() # set plot to animated

# print available ports
#print("Avaiable ports:\n%s"%"\n".join(["\t%d: %s"% (portIndex,str(ports[portIndex])) for portIndex in range(len(ports))]))

selectedDevice = ports[selectedPortIndex].device
print("Selected device: %s"%selectedDevice)

# select device port
ser = serial.Serial(selectedDevice, 9600)

timeCount = 0
timeHist = []
tempAnalHist = []
tempDigHist = []
humidityHist = []
dewPointHist = []
for line in ser:
 entry = line.decode("utf-8").split("\t")
 tempAnal = float(entry[0])
 #tempAnal = float(tempAnal.split()[1])
 humidity = float(entry[1])
 #humidity = float(humidity.split()[1])
 tempDig = float(entry[2])
 #tempDig = float(tempDig.split()[1])
 time = float(entry[3])
 #time = float(time.split()[1])
 timeCount += time/1000

 # magnus formula for dewpoint
 dewPoint = 243.04*(np.log(humidity/100.0)+((17.625*tempAnal)/(243.04+tempAnal)))/(17.625-np.log(humidity/100.0)-((17.625*tempAnal)/(243.04+tempAnal))) 
 
 # single plot
 #print tempAnal,humidity,tempDig
 #plt.plot(timeCount,tempAnal,'bo')
 #plt.axis([0.0,300.0,22,35])

 # data history and plot with line
 timeHist.append(timeCount)
 tempAnalHist.append(tempAnal)
 tempDigHist.append(tempDig)
 humidityHist.append(humidity)
 dewPointHist.append(dewPoint)

 fig, ax1 = plt.subplots()
 ax1.plot(timeHist,tempAnalHist,'b-',label='temperature')
 ax1.plot(timeHist,dewPointHist,'g-',label='dew point')
 ax1.plot(timeHist,tempDigHist,'y-',label='digital temp')
 ax1.axis([min(timeHist)*0.95,
           max(timeHist)*1.05,
           min(dewPointHist)*0.95,
           max(tempDigHist)*1.05])
 ax1.set_xlabel('time[s]')
 ax1.set_ylabel('temperature[*C]')

 ax2 = ax1.twinx()
 ax2.plot(timeHist,humidityHist,'r-',label='humidity')
 ax2.axis([min(timeHist)*0.95,
           max(timeHist)*1.05,
           min(humidityHist)*0.95,
           max(humidityHist)*1.05])
 ax2.set_ylabel('humidity[%]')
 h1, l1 = ax1.get_legend_handles_labels()
 h2, l2 = ax2.get_legend_handles_labels()
 ax1.legend(h1+h2, l1+l2, loc=1)


 #file = 'plot' + str(i) + '.png'
 #plt.savefig(file)
 #plt.close()
 fig.tight_layout()
 plt.pause(time/1000)
 plt.close()
 print timeCount

