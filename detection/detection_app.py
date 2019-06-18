from flask import Flask, redirect, url_for, request, render_template, jsonify, session, make_response, send_file
from werkzeug import security
from werkzeug.utils import secure_filename
import os
import requests
import cv2
import numpy as np
from json import dumps
import math

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

############ Utility functions ############
def load_network(weight_path):

	net = cv2.dnn.readNet(weight_path)

	return net

def decode(scores, geometry, scoreThresh):
    detections = []
    confidences = []

    ############ CHECK DIMENSIONS AND SHAPES OF geometry AND scores ############
    assert len(scores.shape) == 4, "Incorrect dimensions of scores"
    assert len(geometry.shape) == 4, "Incorrect dimensions of geometry"
    assert scores.shape[0] == 1, "Invalid dimensions of scores"
    assert geometry.shape[0] == 1, "Invalid dimensions of geometry"
    assert scores.shape[1] == 1, "Invalid dimensions of scores"
    assert geometry.shape[1] == 5, "Invalid dimensions of geometry"
    assert scores.shape[2] == geometry.shape[2], "Invalid dimensions of scores and geometry"
    assert scores.shape[3] == geometry.shape[3], "Invalid dimensions of scores and geometry"
    height = scores.shape[2]
    width = scores.shape[3]
    for y in range(0, height):

        # Extract data from scores
        scoresData = scores[0][0][y]
        x0_data = geometry[0][0][y]
        x1_data = geometry[0][1][y]
        x2_data = geometry[0][2][y]
        x3_data = geometry[0][3][y]
        anglesData = geometry[0][4][y]
        for x in range(0, width):
            score = scoresData[x]

            # If score is lower than threshold score, move to next x
            if(score < scoreThresh):
                continue

            # Calculate offset
            offsetX = x * 4.0
            offsetY = y * 4.0
            angle = anglesData[x]

            # Calculate cos and sin of angle
            cosA = math.cos(angle)
            sinA = math.sin(angle)
            h = x0_data[x] + x2_data[x]
            w = x1_data[x] + x3_data[x]

            # Calculate offset
            offset = ([offsetX + cosA * x1_data[x] + sinA * x2_data[x], offsetY - sinA * x1_data[x] + cosA * x2_data[x]])

            # Find points for rectangle
            p1 = (-sinA * h + offset[0], -cosA * h + offset[1])
            p3 = (-cosA * w + offset[0],  sinA * w + offset[1])
            center = (0.5*(p1[0]+p3[0]), 0.5*(p1[1]+p3[1]))
            detections.append((center, (w,h), -1*angle * 180.0 / math.pi))
            confidences.append(float(score))

    # Return detections and confidences
    return [detections, confidences]



@app.route('/txt_detection', methods=['GET', 'POST'])
def txt_detection():
	im_name = request.files["field_name"]
	UPLOAD_FOLDER = os.path.join(os.path.join(APP_ROOT,'static'),'image')
	WEIGHT_FOLDER = os.path.join(os.path.join(APP_ROOT,'static'),'weight')

	im_name.save(os.path.join(UPLOAD_FOLDER, 'tmp.jpg'))
	bgr_im = cv2.imread(os.path.join(UPLOAD_FOLDER, 'tmp.jpg'))

	bgr_im = cv2.resize(bgr_im, (1280,1280))
	inpWidth = 1280
	inpHeight = 1280


	net = load_network(os.path.join(WEIGHT_FOLDER,"frozen_east_text_detection.pb"))

	# input image preparation
	blob = cv2.dnn.blobFromImage(bgr_im, 1.0, (inpWidth, inpHeight), (123.68, 116.78, 103.94), True, False)

	outputLayers = []
	outputLayers.append("feature_fusion/Conv_7/Sigmoid")
	outputLayers.append("feature_fusion/concat_3")

	# get outputs (boxes and their scores)
	net.setInput(blob)
	output = net.forward(outputLayers)

	scores = output[0]
	geometry = output[1]

	confThreshold = 0.5
	nmsThreshold = 0.3

	[boxes, confidences] = decode(scores, geometry, confThreshold)
	indices = cv2.dnn.NMSBoxesRotated(boxes, confidences, confThreshold, nmsThreshold)
	print("LEN: ", len(boxes))

	binary_mask = np.zeros((bgr_im.shape[0],bgr_im.shape[1]))
	for i in indices:
		vertices = cv2.boxPoints(boxes[i[0]])
		print(vertices)
		cv2.fillPoly(binary_mask, np.array([vertices]).astype(np.int32), (255))

	for i in indices:
	    # get 4 corners of the rotated rect
	    vertices = cv2.boxPoints(boxes[i[0]])
	    for j in range(4):
	    	vertices[j][0] *= 1
	    	vertices[j][1] *= 1
	    	for j in range(4):
	    		p1 = (vertices[j][0], vertices[j][1])
	    		p2 = (vertices[(j + 1) % 4][0], vertices[(j + 1) % 4][1])
	    		cv2.line(bgr_im, p1, p2, (0, 255, 0), 2, cv2.LINE_AA)

	cv2.imwrite(os.path.join(UPLOAD_FOLDER, 'Original_BB.jpg'), bgr_im)
	cv2.imwrite(os.path.join(UPLOAD_FOLDER, 'Binary_Mask.jpg'), binary_mask)

	
	return 'Detection Success!..'

@app.route('/get_txt_detection', methods=['GET', 'POST'])
def get_txt_detection():
	
	UPLOAD_FOLDER = os.path.join(os.path.join(APP_ROOT,'static'),'image')
	filename = "Gray_Image.jpg"
	path_img = os.path.join(UPLOAD_FOLDER, filename)

	gray_im = cv2.imread(os.path.join(UPLOAD_FOLDER, 'Binary_Mask.jpg'),0)

	print(gray_im.shape)

	# encode image as jpeg
	_, img_encoded = cv2.imencode('.jpg', gray_im)

	#return send_file(os.path.join(UPLOAD_FOLDER, 'Gray_Image.jpg'), mimetype='image/jpg', attachment_filename='Gray_Image.jpg')
	#ilename = os.path.join(UPLOAD_FOLDER, 'Gray_Image.jpg')
	#return send_file(filename, mimetype='image/jpg')

	return img_encoded.tostring()

if __name__ == '__main__':
   app.run(host='0.0.0.0',port=80, debug=True)
