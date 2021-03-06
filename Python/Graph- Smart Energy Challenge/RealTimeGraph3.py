"""
Graphing requires Matplotlib. Run the 2 statements below in cmd (Assuming Python has already been installed)
py -m pip install -U pip setuptools
py -m pip install matplotlib
"""

import matplotlib.pyplot as plt #import the matplotlib library
import numpy as np				#import the numpy extension
from matplotlib.widgets import Button #import the button widget
import warnings
warnings.filterwarnings("ignore") 

try:	
	fig, ax = plt.subplots()	#Create a figure with a set of subplots already made
	plt.subplots_adjust(bottom=0.2) #Adjust the distance from the bottom of the graph to the bottom of the window
	#ax.set_axis_bgcolor('white')	
	#ax.patch.set_facecolor('grey')
	
	t = list(range(300))	#x-axis data points
	
	p = np.sin(t) #represents power array
	v = np.array(t)	#represents voltage array
	a = np.array(t)**2 #represents current array
		
	l, = plt.plot(t, p, lw =3)	#plots a line on the axes with a linewidth of 3
	
	#The initial graph on startup will be a Power vs Time graph
	displayingCurrent = False	#These 3 status variables indicate whether power, voltage or current data is being displayed
	displayingVoltage = False	#and are used by the program when updating the graph to ensure that the correct 
	displayingPower = True		#dataset is being drawn
	
	ax.set_xlim(0, 26)			#The x and y limits for the Power vs Time graph is set
	ax.set_ylim(0, 10)
	txt = fig.text(0.4,0.95,' Power vs Time ',bbox=dict(facecolor='none', alpha=10,lw = 0),fontsize = 15)	
	plt.xlabel('Data Points')
	plt.ylabel('Power (Watts)')
	

	class Index(object):
		#The 5 below functions are used to adjust the x-axis limits depending on the button that is pressed
		def three_hundred(self, event):			
			ax.set_xlim(0, 301)
		def two_hundred(self, event):			
			ax.set_xlim(0, 201)
		def one_hundred(self, event):			
			ax.set_xlim(0, 101)
		def fifty(self, event):			
			ax.set_xlim(0, 51)
		def twenty_five(self, event):			
			ax.set_xlim(0, 26)
		
		#The 3 below functions are used to switch between power, voltage or current graphs depending on which button is pressed
		def voltage(self,event):
			l.set_ydata(v)
			ax.set_ylim(0, 16)
			txt.text.remove()
			txt = fig.text(0.4,0.95,'Voltage vs Time',bbox=dict(facecolor='none', alpha=10,lw=0),fontsize = 15)
			
			#ax.ylabel('Voltage (Volts)')
			global displayingCurrent 
			global displayingVoltage 
			global displayingPower 
			displayingCurrent = False
			displayingVoltage = True
			displayingPower = False
		def current(self,event):
			l.set_ydata(a)
			ax.set_ylim(0, 1.5)
			txt = fig.text(0.4,0.95,'Current vs Time',bbox=dict(facecolor='none', alpha=10,lw=0),fontsize = 15)
			#l.ylabel('Current (Amperes)')
			global displayingCurrent 
			global displayingVoltage 
			global displayingPower 
			displayingCurrent = True
			displayingVoltage = False
			displayingPower = False
			
		def power(self,event):
			l.set_ydata(p)
			ax.set_ylim(0, 10)
			txt = fig.text(0.4,0.95,' Power vs Time ',bbox=dict(facecolor='none', alpha=10,lw = 0),fontsize = 15)	
			#l.ylabel('Power (Watts)')
			global displayingCurrent 
			global displayingVoltage 
			global displayingPower 
			displayingCurrent = False
			displayingVoltage = False
			displayingPower = True
		def close(self,event):
			plt.ioff()
			plt.close()
						
			
		
	callback = Index()
	
	
	ax25 = plt.axes([0.01, 0.01, 0.12, 0.05])
	ax50 = plt.axes([0.14, 0.01, 0.12, 0.05])
	ax100 = plt.axes([0.27, 0.01, 0.12, 0.05])
	ax200 = plt.axes([0.4, 0.01, 0.12, 0.05])
	ax300 = plt.axes([0.53, 0.01, 0.12, 0.05])
	axclose = plt.axes([0.8, 0.01, 0.12, 0.05])
	
	axvoltage = plt.axes([0.01, 0.08, 0.12, 0.05])
	axcurrent = plt.axes([0.14, 0.08, 0.12, 0.05])
	axpower = plt.axes([0.27, 0.08, 0.12, 0.05])
	
	bclose = Button(axclose, 'Close')
	bclose.on_clicked(callback.close)
	bvoltage = Button(axvoltage, 'Voltage')
	bvoltage.on_clicked(callback.voltage)
	bcurrent = Button(axcurrent, 'Current')
	bcurrent.on_clicked(callback.current)
	bpower = Button(axpower, 'Power')
	bpower.on_clicked(callback.power)
	
	b300 = Button(ax300, '300 Points')
	b300.on_clicked(callback.three_hundred)
	b200 = Button(ax200, '200 Points')
	b200.on_clicked(callback.two_hundred)
	b100 = Button(ax100, '100 Points')
	b100.on_clicked(callback.one_hundred)
	b50 = Button(ax50, '50 Points')
	b50.on_clicked(callback.fifty)
	b25 = Button(ax25, '25 Points')
	b25.on_clicked(callback.twenty_five)

	
	plt.ion() #Call plt.ion() in order to enable interactive plotting
	
	
	
	k = 0
	while True:
		
		k+=1
		#if i==10:
			#s[150:300] = 0
		#print(k)
		if displayingCurrent:
			
			#l.set_xdata(t)
			
			l.set_ydata(a)
			#plt.title('Current vs Time')	
			#l.ylabel('Current (Amperes)')
		elif displayingVoltage:
			l.set_ydata(v)
			#txt = fig.text(0.4,0.95,'Voltage vs Time',bbox=dict(facecolor='red', alpha=10),fontsize = 15)
			#l.ylabel('Voltage (Volts)')
		elif displayingPower:
			l.set_ydata(p)
			#l.ylabel('Power (Watts)')
		plt.pause(0.1) #Call plot.pause(0.05) to both draw the new data and it runs the GUI's event loop (allowing for mouse interaction)
		#p[10:300] = 0
		p[0]=10
		l.set_ydata(p[0:301])
		#l.set_xdata(t[0:301])
		#plt.draw()
		plt.pause(0.1)
		#p.pop()
		#p[10:300] = 5
		p[0]=0
		l.set_ydata(p[0:301])
	
except:
	pass
	#print("Graph Closed")	