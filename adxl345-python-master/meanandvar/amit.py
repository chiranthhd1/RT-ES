# ADXL345 Python example
#
# author:  Jonathan Williamson
# license: BSD, see LICENSE.txt included in this package
#
# This is an example to show you how to use our ADXL345 Python library
# http://shop.pimoroni.com/products/adafruit-triple-axis-accelerometer

import time
import math
import numpy
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

pinlist =11

#for i in pinlist:	
GPIO.setup(11,GPIO.OUT)
GPIO.output(11,GPIO.HIGH)

from adxl345 import ADXL345
from array import*

from datetime import datetime

adxl345 = ADXL345()

print "ADXL345 on address 0x%x:" %(adxl345.address)
file = open("updown2.csv",'w')

my_arrayX = [0] * 100;
my_arrayY = [0] * 100;
my_arrayZ = [0] * 100;

xMean = 0
yMean = 0
zMean = 0

xVar = 0
yVar = 0
zVar = 0

counter = 0

Threshold = 0.1

def checkznegpos():
		print ("checking z pos or neg")
		time.sleep(2)
		for i in range (75):
			axes = adxl345.getAxes(True)
			my_arrayX[i] = axes['x']
			my_arrayY[i] = axes['y']
			my_arrayZ[i] = axes['z']
			time.sleep(.04)
		#xMean = numpy.mean(my_arrayX[0:24]);
		#yMean = numpy.mean(my_arrayY[0:24]);
		zMean = numpy.mean(my_arrayZ[0:24]);
		return zMean

def checkynegpos():
		print ("checking y pos or neg")
		time.sleep(2)
		for i in range (100):
			axes = adxl345.getAxes(True)
			my_arrayX[i] = axes['x']
			my_arrayY[i] = axes['y']
			my_arrayZ[i] = axes['z']
			time.sleep(.04)
		#xMean = numpy.mean(my_arrayX[0:24]);
		yMean = numpy.mean(my_arrayY[0:24]);
		#zMean = numpy.mean(my_arrayZ[0:24]);
		return yMean


def operations():
	
	time.sleep(2)
	count =0
	while count<20:
		total = 0
		counterop = 0
		print ("i am in operations")
		for i in range (25):
			axes = adxl345.getAxes(True)
			my_arrayX[i] = axes['x']
			my_arrayY[i] = axes['y']
			my_arrayZ[i] = axes['z']
			time.sleep(.02)

		#xMean = statistics.variance(my_arrayX[0:24]);
		#yMean = statistics.variance(my_arrayY[0:24]);
		#zMean = statistics.variance(my_arrayZ[0:24]);

		xMean = numpy.mean(my_arrayX[0:24]);
		yMean = numpy.mean(my_arrayY[0:24]);
		zMean = numpy.mean(my_arrayZ[0:24]);



		xVar = numpy.var(my_arrayX[0:24]);
		yVar = numpy.var(my_arrayY[0:24]);
		zVar = numpy.var(my_arrayZ[0:24]);

		print "  Inside operations   count = %.3f  xMean = %.3f    yMean = %.3f    zMean = %.3f    xVar = %.3f    yVar = %.3f    zVar = %.3f" % ( count,xMean, yMean, zMean, xVar, yVar, zVar )

		if xVar >= Threshold:
			total = total + 1
		if yVar >= Threshold:
			total = total + 2
		if zVar >= Threshold:
			total = total + 4
		count = count+1
		#counterop = counterop + 1
		#print " counterop = %.3f" %( counterop )
		#if counterop >= 2:
			#print ("############initiated operations################# ")
			#counter=0
		if total == 1:
			print (" ###############  X is UP###########")
			return
		elif total == 2:
			print (" ********* Y is UPPP ******* ")
			yCheck = checkynegpos()
			if yCheck <=  0:
				print ( " ******* y and y-ve is upppp ****")
				GPIO.output(11,GPIO.HIGH)
				return
			else:
			 	print ( " ******* y and y+ve is upppp ****")
				GPIO.output(11,GPIO.LOW)
				return
			
		elif total == 4:
			print ( " ******* z is upppp ****")
			zCheck = checkznegpos()
			if zCheck <=  0:
				print ( " ******* z and z-ve is upppp ****")
				GPIO.output(11,GPIO.HIGH)
				return
			else:
			 	print ( " ******* z and z+ve is upppp ****")
				#gpio0 = 0
				GPIO.output(11,GPIO.LOW)
				return
			
		elif total == 3:
			print ( " *******  XX YY  is upppp ****")
			return 
		elif total == 5:
			print ( " ******* XX ZZ is upppp ****")
			return 
		elif total == 6:
			print ( " ******* YY ZZ is upppp ****")
			return 
		elif total == 7:
			print ( " ******* all  is well ****")
			#counterop = 0
			#print("operation() completed ")
			return
		

while True:
	ymean=0
	ysum =0
        
	#for loop runs for 25 times and
	#collects 25 individual readings of X, Y and Z
	for i in range (24):
		axes = adxl345.getAxes(True)
		my_arrayX[i] = axes['x']
		my_arrayY[i] = axes['y']
		my_arrayZ[i] = axes['z']
		time.sleep(.01)

	#xMean = statistics.variance(my_arrayX[0:24]);
	#yMean = statistics.variance(my_arrayY[0:24]);
	#zMean = statistics.variance(my_arrayZ[0:24]);
	
	xMean = numpy.mean(my_arrayX[0:24]);
	yMean = numpy.mean(my_arrayY[0:24]);
	zMean = numpy.mean(my_arrayZ[0:24]);
	
	
	
	xVar = numpy.var(my_arrayX[0:24]);
	yVar = numpy.var(my_arrayY[0:24]);
	zVar = numpy.var(my_arrayZ[0:24]);
	
	#xVar = statistics.variance(my_arrayX[0:24]);
	#yVar = statistics.variance(my_arrayY[0:24]);
	#zVar = statistics.variance(my_arrayZ[0:24]);
	
	#print ("         xMean = {}    yMean = {}    zMean = {}    xVar = {}    yVar = {}    zVar = {}" .format ( xMean, yMean, zMean, xVar, yVar, zVar ))
	print "         xMean = %.3f    yMean = %.3f    zMean = %.3f    xVar = %.3f    yVar = %.3f    zVar = %.3f" % ( xMean, yMean, zMean, xVar, yVar, zVar )
 
	if yVar >= Threshold or xVar >= Threshold or zVar >= Threshold :
		counter=counter+1
		print " counter = %.3f" %( counter )
		if counter >= 5:
			print ("############initiated operations################# ")
			operations()
			counter = 0
			print("operation() completed ")
		else:
			continue
	else:
		counter=0

GPIO.cleanup()
