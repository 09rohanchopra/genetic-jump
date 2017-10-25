import mss
import mss.tools
from PIL import Image
import pyautogui as pa
from time import sleep
import csv
from pynput import keyboard

count = 0
press0 = 0
press1 = 0

# Create file
with open('keys.csv', 'w') as csvfile:
	fieldnames = ['up', 'down', 'image']
	writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
	writer.writeheader()

def snap(path):
	with mss.mss() as sct:
	    # The screen part to capture
		monitor = {'top': 150, 'left': 650, 'width': 620, 'height': 150}
		num =1
	    # Grab the data
		sct_img = sct.grab(monitor)
		img = Image.frombytes('RGB', sct_img.size, sct_img.rgb) # get the screenshot of gaming port (620 x 100)
		img2 = img.resize((124,20), Image.BICUBIC)	# resize to 124 x 20 (you can try other filters like ANTIALIAS, BILINEAR, NEAREST)
		img2.save(path, "PNG") # save the screeenshot

# callback for handling key presses
def on_press(key):
	global press0, press1
	if key == keyboard.Key.up:
		press0 = 1
		press1 = 0
	elif key == keyboard.Key.down:
		press0 = 0
		press1 = 1
	else:
		press0 = 0
		press1 = 0

# callback for handling key release
def on_release(key):
	global press0, press1
	press0 = 0
	press1 = 0
	if key == keyboard.Key.esc:
		return False

# Function to apeend to create dataset file
def csv_writer(press0, press1, image):
	with open('keys.csv', 'a') as csvfile:
		fieldnames = ['up', 'down', 'image']
		writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
		writer.writerow({'up' : press0, 'down' : press1, 'image' : image})


pa.click(300,300)
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
	while True:
		path = 'snaps/' + str(count)
		snap(path)
		csv_writer(press0, press1, path)
		#print ('{}, {}, '.format(press0, press1) + path)
		count=count+1
		sleep(0.03)

listener.join()
