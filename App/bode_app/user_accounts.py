# background: linear-gradient(to right, #b92b27, #1565c0)
from . import bode
from flask import request, render_template


@bode.route('/', methods=['POST', 'GET'])
def login():
    print('request')
    if request.method == 'GET':
        return render_template('Login.html')
    elif request.method == 'POST':
        username = request.form.get("login-username", '')
        password = request.form.get("login-password", '')
        print(username, password)
        return render_template('User_Profile.html', name='Test1')

 def logincheck(x,y):
  for g in x:
    if g == x:
      return loginin
    if g!= x:
      print("Inaccurate login in. Try again")

def loginin(x,y):
  for z in x:
    return z 
