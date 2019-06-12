from flask import Flask,flash,redirect, url_for, request, render_template, jsonify, session
from werkzeug import security
from werkzeug.utils import secure_filename
import os
import requests
import cv2
import numpy as np
import PIL.Image

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))



@app.route('/master')
def master():
   return render_template('knockout_1.html')


@app.route("/upload")
def upload_image():
   print("Upload Controller Working")
   return render_template('upload.html')


@app.route('/image_app', methods = ['GET', 'POST'])
def upload_img():

   print("Image app")
   UPLOAD_FOLDER = os.path.join(os.path.join(APP_ROOT,'static'),'image')

   if request.method == 'POST':
      # check if the post request has the file part
      if 'file' not in request.files:
         print('No file part')
         return jsonify({'result' : 'No file part!..'})
      file = request.files['file']
      # if user does not select file, browser also
      # submit a empty part without filename
      if file.filename == '':
         print('No selected file')
         return jsonify({'result' : 'No selected file!..'})

      if file:
         filename = secure_filename(file.filename)
         file.save(os.path.join(UPLOAD_FOLDER, filename))
         #file.save(os.path.join(UPLOAD_FOLDER, "img.jpg"))

   return jsonify({"result":"Saving O.k.", "filename": file.filename})
   #return jsonify({"result":"Saving O.k.", "filename": "img.jpg"})


@app.route('/uploader_app', methods = ['GET', 'POST'])
def upload_item():
   print("Uploader Controller")

   if request.method == 'POST':

      data = request.get_json()

      name = data['yourName']
      surname = data['yourSurname']

   #return jsonify({'result' : 'Success!..'})
   print(name)
   print(surname)
   return render_template('knockout_1.html')

@app.route('/image_delete', methods = ['GET', 'POST'])
def delete_img():

   print("Image delete")
   UPLOAD_FOLDER = os.path.join(os.path.join(APP_ROOT,'static'),'image')

   if request.method == 'POST':
      # check if the post request has the file part
      if not(os.path.isdir(UPLOAD_FOLDER)):
         print('No such a directory')
         return jsonify({'result' : 'No such a directory!..'})
      files = os.listdir(UPLOAD_FOLDER)
      print("There are # files:", len(files))

      for the_file in os.listdir(UPLOAD_FOLDER):
         file_path = os.path.join(UPLOAD_FOLDER, the_file)
         try:
            if os.path.isfile(file_path):
               os.unlink(file_path)
            # elif os.path.isdir(file_path): shutil.rmtree(file_path)
         except Exception as e:
            print(e)

   return jsonify({"result":"Deletion O.k."})

############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################

@app.route('/gray_convert', methods=['GET', 'POST'])
def index(): 
	st_code = 0

	UPLOAD_FOLDER = os.path.join(os.path.join(APP_ROOT,'static'),'image')
	filename = os.listdir(UPLOAD_FOLDER)[0]
	print(filename)
	path_img = os.path.join(UPLOAD_FOLDER, filename)
	
	with open(path_img, "rb") as image_file:
		files = {'field_name': image_file}

		r = requests.post('http://gr/create_grayscale', files=files )
		#print(r.status_code)
		txt = r.text
		print(txt)
	
	return jsonify({"result":"Grayscale Conversation O.k."})


@app.route('/get_gray_convert', methods=['GET', 'POST'])
def get_index(): 
	UPLOAD_FOLDER = os.path.join(os.path.join(APP_ROOT,'static'),'image')
	
	r = requests.get('http://gr/getting_gray_convert')

	#nparr = np.fromstring(r.data, np.uint8)
	#im_gray = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	#print(r.content.tofile().shape)
	#decoded = cv2.imdecode(np.frombuffer(r.content, np.uint8), -1)
	decoded = np.fromstring(r.content, np.uint8)
	decoded = cv2.imdecode(decoded, 0)
	
	cv2.imwrite(os.path.join(UPLOAD_FOLDER, 'Gray_Image.jpg'), decoded)

	
	return jsonify({"result":"Getting Grayscale Conversation O.k."})

############################################################################################################

@app.route('/sharp', methods=['GET', 'POST'])
def index_sharp(): 
	st_code = 0

	UPLOAD_FOLDER = os.path.join(os.path.join(APP_ROOT,'static'),'image')
	filename = os.listdir(UPLOAD_FOLDER)[0]
	print(filename)
	path_img = os.path.join(UPLOAD_FOLDER, filename)

	
	with open(path_img, "rb") as image_file:
		files = {'field_name': image_file}

		r = requests.post('http://sh/create_sharp', files=files )
		#print(r.status_code)
		txt = r.text
		print(txt)
	
	return jsonify({"result":"Sharpening O.k.", "path":os.path.join(UPLOAD_FOLDER, "Sharp_Image.jpg")})


@app.route('/get_sharp_convert', methods=['GET', 'POST'])
def get_index_sharp(): 
	UPLOAD_FOLDER = os.path.join(os.path.join(APP_ROOT,'static'),'image')
	
	r = requests.get('http://sh/getting_sharp_convert')

	#nparr = np.fromstring(r.data, np.uint8)
	#im_gray = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	#print(r.content.tofile().shape)
	#decoded = cv2.imdecode(np.frombuffer(r.content, np.uint8), -1)
	decoded = np.fromstring(r.content, np.uint8)
	decoded = cv2.imdecode(decoded, 0)
	
	cv2.imwrite(os.path.join(UPLOAD_FOLDER, 'Sharp_Image.jpg'), decoded)

	
	return jsonify({"result":"Getting Sharp Image O.k."})
############################################################################################################

@app.route('/blur', methods=['GET', 'POST'])
def index_blur(): 
	st_code = 0

	UPLOAD_FOLDER = os.path.join(os.path.join(APP_ROOT,'static'),'image')
	filename = os.listdir(UPLOAD_FOLDER)[0]
	print(filename)
	path_img = os.path.join(UPLOAD_FOLDER, filename)
	
	with open(path_img, "rb") as image_file:
		files = {'field_name': image_file}

		r = requests.post('http://bl/create_blur', files=files )
		#print(r.status_code)
		txt = r.text
		print(txt)

	
	return jsonify({"result":"Blurring O.k.", "path":os.path.join(UPLOAD_FOLDER, "Blur_Image.jpg")})


@app.route('/get_blur_convert', methods=['GET', 'POST'])
def get_index_blur(): 
	UPLOAD_FOLDER = os.path.join(os.path.join(APP_ROOT,'static'),'image')
	
	r = requests.get('http://bl/getting_blur_convert')

	#nparr = np.fromstring(r.data, np.uint8)
	#im_gray = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	#print(r.content.tofile().shape)
	#decoded = cv2.imdecode(np.frombuffer(r.content, np.uint8), -1)
	decoded = np.fromstring(r.content, np.uint8)
	decoded = cv2.imdecode(decoded, 1)
	
	cv2.imwrite(os.path.join(UPLOAD_FOLDER, 'Blur_Image.jpg'), decoded)

	
	return jsonify({"result":"Getting blur Image O.k."})


############################################################################################################

@app.route('/edge', methods=['GET', 'POST'])
def index_edge(): 
	st_code = 0

	UPLOAD_FOLDER = os.path.join(os.path.join(APP_ROOT,'static'),'image')
	filename = os.listdir(UPLOAD_FOLDER)[0]
	print(filename)
	path_img = os.path.join(UPLOAD_FOLDER, filename)


	
	with open(path_img, "rb") as image_file:
		files = {'field_name': image_file}

		r = requests.post('http://ed/create_edge', files=files )
		#print(r.status_code)
		txt = r.text
		print(txt)
	
	return jsonify({"result":"Edge Map Extraction O.k.", "path":os.path.join(UPLOAD_FOLDER, "Edge_Image.jpg")})

@app.route('/get_edge_convert', methods=['GET', 'POST'])
def get_index_edge(): 
	UPLOAD_FOLDER = os.path.join(os.path.join(APP_ROOT,'static'),'image')
	
	r = requests.get('http://ed/getting_edge_convert')

	#nparr = np.fromstring(r.data, np.uint8)
	#im_gray = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	#print(r.content.tofile().shape)
	#decoded = cv2.imdecode(np.frombuffer(r.content, np.uint8), -1)
	decoded = np.fromstring(r.content, np.uint8)
	decoded = cv2.imdecode(decoded, 0)
	
	cv2.imwrite(os.path.join(UPLOAD_FOLDER, 'Edge_Image.jpg'), decoded)

	
	return jsonify({"result":"Getting Edge Image O.k."})

############################################################################################################

@app.route('/saliency', methods=['GET', 'POST'])
def index_saliency(): 
	st_code = 0

	UPLOAD_FOLDER = os.path.join(os.path.join(APP_ROOT,'static'),'image')
	filename = os.listdir(UPLOAD_FOLDER)[0]
	print(filename)
	path_img = os.path.join(UPLOAD_FOLDER, filename)
	
	with open(path_img, "rb") as image_file:
		files = {'field_name': image_file}

		r = requests.post('http://sa/create_saliency', files=files )
		#print(r.status_code)
		txt = r.text
		print(txt)
	
	return jsonify({"result":"Saliency Map O.k.", "path":os.path.join(UPLOAD_FOLDER, "Saliency_Image.jpg")})


@app.route('/get_saliency_convert', methods=['GET', 'POST'])
def get_index_saliency(): 
	UPLOAD_FOLDER = os.path.join(os.path.join(APP_ROOT,'static'),'image')
	
	r = requests.get('http://sa/getting_saliency_convert')

	#nparr = np.fromstring(r.data, np.uint8)
	#im_gray = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	#print(r.content.tofile().shape)
	#decoded = cv2.imdecode(np.frombuffer(r.content, np.uint8), -1)
	decoded = np.fromstring(r.content, np.uint8)
	decoded = cv2.imdecode(decoded, 0)
	
	cv2.imwrite(os.path.join(UPLOAD_FOLDER, 'Saliency_Image.jpg'), decoded)

	
	return jsonify({"result":"Getting Saliency Image O.k."})

############################################################################################################


if __name__ == '__main__':
   app.run(host='0.0.0.0',port=80, debug=True)
