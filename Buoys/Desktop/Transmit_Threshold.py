import RPi.GPIO as GPIO
import time
import os
import numpy as np
#from scipy.signal import freqz, butter, lfilter
from scipy.fftpack import fft

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, 0)


source = "/home/pi/Documents/Data/"
drive = "/media/pi/usb/1/"
d_time = 0

#def butter_bandpass(lowcut, highcut, fs, order=5):
#    nyq = 0.5 * fs
#    low = lowcut / nyq
#    high = highcut / nyq
#    b, a = butter(order, [low, high], btype='band')
#   return b, a

#def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
#    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
#    y = lfilter(b, a, data)
#    return y	

def threshold(signal,fs,lowcut,highcut,threshold):
	v = np.genfromtxt(signal, delimiter=",",skip_header=5, usecols=(0), unpack=True)
	#v_filtered = butter_bandpass_filter(v, lowcut, highcut, fs, order=6)
	v_fft= np.abs(fft(v))
	if (v_fft >= threshold).any() == True:
		return "Possible Whale Detected: Send File"
		scp = "sudo sshpass -p '******' scp /home/pi/Documents/Data/%s.txt.bz2 whale-srv@******:~/Whale_Srv/Incoming/1/" % d_time
		os.system(scp)
		print("FILE SENT!")
	else:
		return "No Whale Detected: Do Not Send File"
		print("FILE NOT SENT!")	
	
def transmit():
	d_time = time.time()
	GPIO.output(18, 1)
	destination = "/home/pi/Documents/Data/%s.txt" % d_time
	os.chdir(source)
       	os.rename("Data.txt", destination)
	zip = "sudo bzip2 %s" % destination
	os.system(zip)
	print("File compressed")
	cp = "sudo cp %s.txt.bz2 /media/pi/usb/1/" % d_time
	os.system(cp)
	print("Saved to USB storage device")
	threshold("/home/pi/Documents/Data/%s.txt.bz2" % d_time,10000,2500,3500,10000)
	GPIO.output(18, 0)
	print("Done! %s" % d_time)
	
transmit()
