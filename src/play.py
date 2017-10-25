import mss
import mss.tools
from PIL import Image
from pynput.keyboard import Key, Controller



import argparse
import numpy as np
from keras.models import load_model
import cv2
from time import sleep

keyboard = Controller()

def snap():
	with mss.mss() as sct:
	    # The screen part to capture
		monitor = {'top': 150, 'left': 650, 'width': 620, 'height': 150}
		num =1
	    # Grab the data
		sct_img = sct.grab(monitor)
		img = Image.frombytes('RGB', sct_img.size, sct_img.rgb) # get the screenshot of gaming port (620 x 100)
		img2 = img.resize((124,20), Image.BICUBIC)	# resize to 124 x 20 (you can try other filters like ANTIALIAS, BILINEAR, NEAREST)
		image = np.array(img2)
		print(image.shape)
		return image

def telemetry():

	image = snap()
	image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	image = image.astype('float32')
	image /= 255.0
	image = image.reshape(-1,20,124,1).astype('float32')

	keys = model.predict(image, batch_size = 1)
	print(keys)

	send_command(keys)

def send_command(keys):

	value = np.argmax(keys[0])
	print(value)
	if value == 1:
		keyboard.press(Key.up)
	elif value == 2:
		keyboard.press(Key.down)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Auto play')
	parser.add_argument(
		'model',
		type=str,
		help='Path to model h5 file. Model should be on the same path.'
	)
	args = parser.parse_args()

	#load model
	model = load_model(args.model)

	while(1):
		telemetry()
	
