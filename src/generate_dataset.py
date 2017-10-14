from pynput import keyboard
import pyautogui as pa
import pyscreenshot as ps
import csv 
import time
press = 0
count = 0

#To bring chrome window forward
pa.click(300,300)

#Create file and add headers
with open('keys.csv', 'w') as csvfile:
	fieldnames = ['key', 'image']
	writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
	writer.writeheader()
  
#Clicks screenshit of game frame
def snap(path):
	img = ps.grab(bbox = (640, 110, 1280, 330))
	img.convert('RGB').save(path)

#Upload key log and image path
def csv_writer(press, image):
	with open('keys.csv', 'a') as csvfile:
		fieldnames = ['key', 'image']
		writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
		writer.writerow({'key' : press, 'image' : image})

#Callback for key press
def on_press(key):
	global count	
	if key == keyboard.Key.up:
		press = 1
	elif key == keyboard.Key.down:
		press = 2
	else: 
		press = 0	
	print (press)
	path = 'snaps/' + str(count) + '.jpg'
	snap(path)
	csv_writer(press, path)
	count=count+1
  
#Callback for key release
def on_release(key):
	press = 0;
	if key == keyboard.Key.esc:
		# Stop listener
		return False
	print (press)	

#Good old key listener
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
