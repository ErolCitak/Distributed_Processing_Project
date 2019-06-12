from flask import Flask, redirect, url_for, request, render_template, jsonify, session
from werkzeug import security
from werkzeug.utils import secure_filename
import os
import requests
import cv2
import numpy as np

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))



@app.route('/create_blur', methods=['GET', 'POST'])
def create_blur():
	im_name = request.files["field_name"]
	UPLOAD_FOLDER = os.path.join(os.path.join(APP_ROOT,'static'),'image')

	im_name.save(os.path.join(UPLOAD_FOLDER, 'tmp.jpg'))
	bgr_im = cv2.imread(os.path.join(UPLOAD_FOLDER, 'tmp.jpg'))

	blur_im = cv2.GaussianBlur(bgr_im,(11,11),3)
	cv2.imwrite(os.path.join(UPLOAD_FOLDER, 'Blur_Image.jpg'), blur_im)
	
	return 'Blurring Success!..'

@app.route('/getting_blur_convert', methods=['GET', 'POST'])
def get_blur_convert():
	
	UPLOAD_FOLDER = os.path.join(os.path.join(APP_ROOT,'static'),'image')
	filename = "Blur_Image.jpg"
	path_img = os.path.join(UPLOAD_FOLDER, filename)

	blur_im = cv2.imread(os.path.join(UPLOAD_FOLDER, 'Blur_Image.jpg'),1)
	print(blur_im.shape)

	# encode image as jpeg
	_, img_encoded = cv2.imencode('.jpg', blur_im)

	#return send_file(os.path.join(UPLOAD_FOLDER, 'Gray_Image.jpg'), mimetype='image/jpg', attachment_filename='Gray_Image.jpg')
	#ilename = os.path.join(UPLOAD_FOLDER, 'Gray_Image.jpg')
	#return send_file(filename, mimetype='image/jpg')

	return img_encoded.tostring()

if __name__ == '__main__':
   app.run(host='0.0.0.0',port=80, debug=True)