import cv2
import numpy
from flask import Flask, redirect, url_for

app: Flask = Flask(__name__)



@app.route('/hello/<int:imageId>')
def hello_world(imageId):

    return "Hello Flask and its Debug mode with Image ID: %d" % imageId


@app.route('/admin')
def hello_admin():
   return 'Hello Admin Kişisi'

@app.route('/guest/<guest>')
def hello_guest(guest):
   return 'Hello %s as Guest' % guest

@app.route('/user/<name>')
def hello_user(name):
   if name =='admin' or name == 'Admin':
      return redirect(url_for('hello_admin'))
   else:
      return redirect(url_for('hello_guest',guest = name))

# app url rules
app.add_url_rule('/','/hello',hello_world)

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8000, debug=True)
