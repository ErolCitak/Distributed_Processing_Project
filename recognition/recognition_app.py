from flask import Flask, redirect, url_for, request, render_template, jsonify, session
from werkzeug import security
from werkzeug.utils import secure_filename
import os
import requests
import cv2
import numpy as np
import pytesseract

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

BINARY_THRESHOLD = 180

def image_smoothing(img):
	ret1, th1 = cv2.threshold(img, 180, 255, cv2.THRESH_BINARY)
	ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	blur = cv2.GaussianBlur(th2, (1,1), 0)
	ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

	return th3

def get_hsv(img, channel):

	return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)[:,:,channel]

@app.route('/txt_recognize', methods=['GET', 'POST'])
def txt_recognize():
	im_bgr = request.files["bgr_image"]
	im_mask = request.files["mask_image"]
	UPLOAD_FOLDER = os.path.join(os.path.join(APP_ROOT,'static'),'image')

	im_bgr.save(os.path.join(UPLOAD_FOLDER, 'tmp.jpg'))
	bgr_im = cv2.imread(os.path.join(UPLOAD_FOLDER, 'tmp.jpg'))

	im_mask.save(os.path.join(UPLOAD_FOLDER, 'tmp_mask.jpg'))
	mask_im = cv2.imread(os.path.join(UPLOAD_FOLDER, 'tmp_mask.jpg'))

	print(mask_im.shape)
	print(np.max(mask_im))

	bgr_im = cv2.resize(bgr_im, (1280,1280))

	# CCA 
	mask_im = cv2.cvtColor(mask_im, cv2.COLOR_BGR2GRAY)
	ret, comp = cv2.connectedComponents(mask_im, 16)

	mask = np.array(comp, dtype=np.uint8)
	for label in range(1, ret):
		mask[comp == label] = 255

	kernel_sqr = np.ones((5,5), np.uint8)
	mask = cv2.dilate(mask, kernel_sqr, iterations=2)
	mask = cv2.erode(mask, kernel_sqr, iterations=2)


	output = open(os.path.join(UPLOAD_FOLDER,"output_text.txt"),"w",encoding="utf-8")
	config = ('-l eng --oem 1 --psm 3')

	# find contours
	contours = cv2.findContours(mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

	padding = 10
	counter = 0
	for cnt in contours:
		(x,y,w,h) = cv2.boundingRect(cnt)

		a = y - padding
		b = x - padding
		c = y + h + padding
		d = x + w + padding

		# If padding exceeds from our borders
		if y - padding < 0:
			a = y
		if x - padding < 0:
			b = x
		if y + h + padding > x:
			c = y + h
		if x + w + padding > y:
			d = x + w

		ROI = bgr_im[a:c, b:d]

		ROI = image_smoothing(get_hsv(ROI,2))

		
		x,y = ROI.shape
		col_val = ROI[0,0]

		if col_val < 128:
			x,y = ROI.shape

			for i in range(x):
				for j in range(y):
					ROI[i,j] = np.abs(255 - ROI[i,j])
		
		kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
		ROI = cv2.filter2D(ROI, -1, kernel)
		
		output.write("- "+ pytesseract.image_to_string(ROI, config=config)+ "\n")
		cv2.imwrite(os.path.join(UPLOAD_FOLDER, 'Sharp_Image'+str(counter)+'.jpg'), ROI)
		counter += 1

	bitwised_image = cv2.bitwise_and(get_hsv(bgr_im,2),mask_im,mask_im)
	cv2.imwrite(os.path.join(UPLOAD_FOLDER, 'Bitwised_Image.jpg'), bitwised_image)
	output.close()
	
	
	return 'Sharpening Success!..'

@app.route('/get_txt_recognize', methods=['GET', 'POST'])
def get_txt_recognize():
	
	UPLOAD_FOLDER = os.path.join(os.path.join(APP_ROOT,'static'),'image')
	filename = "Sharp_Image.jpg"
	path_img = os.path.join(UPLOAD_FOLDER, filename)

	sharp_im = cv2.imread(os.path.join(UPLOAD_FOLDER, 'Sharp_Image.jpg'),0)
	print(sharp_im.shape)

	# encode image as jpeg
	_, img_encoded = cv2.imencode('.jpg', sharp_im)

	#return send_file(os.path.join(UPLOAD_FOLDER, 'Gray_Image.jpg'), mimetype='image/jpg', attachment_filename='Gray_Image.jpg')
	#ilename = os.path.join(UPLOAD_FOLDER, 'Gray_Image.jpg')
	#return send_file(filename, mimetype='image/jpg')

	return img_encoded.tostring()

if __name__ == '__main__':
   app.run(host='0.0.0.0',port=80, debug=True)
