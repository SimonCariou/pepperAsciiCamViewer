import qi
from auth import *
from PIL import Image
import time
import sys

#######

class pepperCam:
	def __init__(self, url, user, pswd):
		#naoqi related variables
		self.session = None
		self.cameraSubscriber = None

		#variables related to image capture:
		self.AL_kTopCamera = 0
		self.AL_kQVGA = 1 # 320x240
		self.AL_kBGRColorSpace = 13
		self.fps = 2	

		#variables related to the image size
		self.imageWidth = None
		self.imageHeight = None
		self.imageArray = None

		#naoqi authentication + camera instanciation
		self.authenticate(url, user, pswd)
		self.camera = self.session.service("ALVideoDevice")

	def authenticate(self, url, user, pswd):
	#url, user, pswd = parse_options()
		factory = ClientFactory(user, pswd)
		self.session = qi.Session()
		self.session.setClientAuthenticatorFactory(factory)
		self.session.connect(url)

	def run(self):
		self.cameraSubscriber = self.camera.subscribeCamera("peppercam", self.AL_kTopCamera, self.AL_kQVGA, self.AL_kBGRColorSpace, self.fps)
		print self.cameraSubscriber

		#set image size for the entire loop:
		result = self.camera.getImageRemote(self.cameraSubscriber)
		self.imageWidth = result[0]
		self.imageHeight = result[1]

		#video loop
		while True:
		# capture image
			try:
				result = self.camera.getImageRemote(self.cameraSubscriber)
				#image capture state verification:
				if result == None:
					print 'cannot capture.'
				elif result[6] == None:
					print 'no image data string.'
				else:
					print 'Image captured'
					# result[6] is the image data
					self.imageArray = result[6]
					self.viewAscii(self.imageArray)
					#sleep for the amount of time given in the variable fps
					time.sleep(0.1)

			except KeyboardInterrupt:
				print "Unsubscribing..."
				self.camera.unsubscribe(self.cameraSubscriber)
				print "done"
				break

	def viewAscii(self, imgArray):
		image_string = str(bytearray(imgArray))

		img = Image.fromstring("RGB", (self.imageWidth, self.imageHeight), image_string) 
		aspect_ratio = self.imageWidth/self.imageHeight
		new_width = 120
		new_height = aspect_ratio * new_width * 0.55
		img = img.resize((new_width, int(new_height)))
		img = img.convert('L')
		pixels = img.getdata()

		# replace each pixel with a character from array
		chars = " .^-;~=+*#%@"
		new_pixels = [chars[pixel//25] for pixel in pixels]
		new_pixels = ''.join(new_pixels)

		# split string of chars into multiple strings of length equal to new width and create a list
		new_pixels_count = len(new_pixels)
		ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
		ascii_image = "\n".join(ascii_image)
		print ascii_image

#######

def main(argv):
	connUrl = "tcps://{}:9503".format(sys.argv[1])
	user = "nao"
	password = "nao"
	camViewer = pepperCam(connUrl, user, password)
	camViewer.run()

if __name__ == "__main__":
	main(sys.argv[1:])
