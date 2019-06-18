from flask import Flask, redirect, url_for, request, render_template, jsonify, session
from werkzeug import security
from werkzeug.utils import secure_filename
import os
import requests
import cv2
import numpy as np

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

BINARY_THRESHOLD = 200

def image_smoothing(img):
	ret1, th1 = cv2.threshold(img, BINARY_THRESHOLD, 255, cv2.THRESH_BINARY)
	ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	blur = cv2.GaussianBlur(th2, (1,1), 0)
	ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

	return th3

@app.route('/txt_preprocess', methods=['GET', 'POST'])
def txt_preprocess():
	im_name = request.files["field_name"]
	UPLOAD_FOLDER = os.path.join(os.path.join(APP_ROOT,'static'),'image')

	im_name.save(os.path.join(UPLOAD_FOLDER, 'tmp.jpg'))
	mask_im = cv2.imread(os.path.join(UPLOAD_FOLDER, 'tmp.jpg'))

	# apply morphological operations onto image
	kernel_sqr = np.ones((5,5), np.uint8)
	kernel_line= np.ones((1,5), np.uint8)
	kernel_line_2 = np.ones((5,1), np.uint8)

	print("a1")

	# Morph. Begins
	img_dilation = cv2.dilate(mask_im, kernel_line, iterations=2)
	img_dilation = cv2.erode(img_dilation, kernel_line, iterations=2)

	img_dilation = cv2.dilate(img_dilation, kernel_line_2, iterations=2)
	img_dilation = cv2.erode(img_dilation, kernel_line_2, iterations=2)

	img_dilation = cv2.dilate(img_dilation, kernel_sqr, iterations=2)
	img_dilation = cv2.erode(img_dilation, kernel_sqr, iterations=2)
	# Morph. Ends

	print("a2")

	# CCA
	#im = cv2.cvtColor(img_dilation, cv2.COLOR_BGR2GRAY)
	"""
	ret, comp = cv2.connectedComponents(img_dilation,16)

	mask_im = np.array(comp, dtype=np.uint8)
	for label in range(1,ret):
		mask_im[comp == label] = 255

	print("a3")

	# morph for cca
	mask_im = cv2.dilate(mask_im, kernel_sqr, iterations=2)
	mask_im = cv2.erode(mask_im, kernel_sqr, iterations=2)
	"""

	cv2.imwrite(os.path.join(UPLOAD_FOLDER, 'Preprocessed_Image.jpg'), img_dilation)
	
	return 'Preprocessing Success!..'

@app.route('/get_txt_preprocess', methods=['GET', 'POST'])
def get_txt_preprocess():
	
	UPLOAD_FOLDER = os.path.join(os.path.join(APP_ROOT,'static'),'image')
	filename = "Preprocessed_Image.jpg"
	path_img = os.path.join(UPLOAD_FOLDER, filename)

	mask_im = cv2.imread(os.path.join(UPLOAD_FOLDER, 'Preprocessed_Image.jpg'),0)
	print(mask_im.shape)

	# encode image as jpeg
	_, img_encoded = cv2.imencode('.jpg', mask_im)

	#return send_file(os.path.join(UPLOAD_FOLDER, 'Gray_Image.jpg'), mimetype='image/jpg', attachment_filename='Gray_Image.jpg')
	#ilename = os.path.join(UPLOAD_FOLDER, 'Gray_Image.jpg')
	#return send_file(filename, mimetype='image/jpg')

	return img_encoded.tostring()

if __name__ == '__main__':
   app.run(host='0.0.0.0',port=80, debug=True)
