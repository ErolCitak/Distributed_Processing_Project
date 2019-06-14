from flask import Flask, redirect, url_for, request, render_template, jsonify, session, make_response, send_file
from werkzeug import security
from werkzeug.utils import secure_filename
import os
import requests
import cv2
import numpy as np
from json import dumps
from eval import main

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))



@app.route('/txt_detection', methods=['GET', 'POST'])
def txt_detection():
	im_name = request.files["field_name"]
	UPLOAD_FOLDER = os.path.join(os.path.join(APP_ROOT,'static'),'image')

	im_name.save(os.path.join(UPLOAD_FOLDER, 'tmp.jpg'))
	bgr_im = cv2.imread(os.path.join(UPLOAD_FOLDER, 'tmp.jpg'))

	main(UPLOAD_FOLDER,'-1','tmp/east_icdar2015_resnet_v1_50_rbox/',os.path.join(APP_ROOT,'static'),False)

	#cv2.imwrite(os.path.join(UPLOAD_FOLDER, 'Gray_Image.jpg'), im_gray)
	
	return 'Detection Success!..'

@app.route('/get_txt_detection', methods=['GET', 'POST'])
def get_txt_detection():
	
	UPLOAD_FOLDER = os.path.join(os.path.join(APP_ROOT,'static'),'image')
	filename = "Gray_Image.jpg"
	path_img = os.path.join(UPLOAD_FOLDER, filename)

	gray_im = cv2.imread(os.path.join(UPLOAD_FOLDER, 'Gray_Image.jpg'),0)
	print(gray_im.shape)

	# encode image as jpeg
	_, img_encoded = cv2.imencode('.jpg', gray_im)

	#return send_file(os.path.join(UPLOAD_FOLDER, 'Gray_Image.jpg'), mimetype='image/jpg', attachment_filename='Gray_Image.jpg')
	#ilename = os.path.join(UPLOAD_FOLDER, 'Gray_Image.jpg')
	#return send_file(filename, mimetype='image/jpg')

	return img_encoded.tostring()

if __name__ == '__main__':
   app.run(host='0.0.0.0',port=80, debug=True)