from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)

@app.route('/success/<uName>')
def success_screen(uName):
   return 'welcome %s' % uName

@app.route('/login',methods = ['POST', 'GET'])
def login_screen():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success_screen', uName = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success_screen', uName = user))

@app.route('/<guestName>')
def index(guestName):
    return render_template('login.html', gName = guestName)

@app.route('/<int:exam_score>')
def exam_result(exam_score):
   return render_template('exam_result.html', marks = exam_score)


if __name__ == '__main__':
   app.run(host='127.0.0.1',port=8000, debug=True)
