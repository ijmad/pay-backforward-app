#!/usr/bin/env python

from flask import Flask, redirect, jsonify, url_for, request
import os

DEMO_APP_URL = os.environ['DEMO_APP_URL']

app = Flask(__name__)
payments = {}

@app.after_request
def cache_headers(response):    
  response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
  response.headers['Pragma'] = 'no-cache'
  return response

@app.route('/start/<int:id>')
def start(id):
    global payments
    if id not in payments:
      payments[id] = { 'found' : True, 'entered_card': False, 'confirmed': False }
    return redirect(url_for('details_get', id=id), code=303)

@app.route('/details/<int:id>')
def details_get(id):
    global payments
    
    if payments[id]['confirmed']:
      if payments[id]['success']:
        return \
          '<html><head><title>Make Payment</title></head>'\
          '<body style=\"font-size: 150%;\">'\
          '  <h1>GOV.UK Pay</h1>'\
          '  <h2>Enter Your Card Details</h2>'\
          '  <p>You already entered your details and confirmed your payment</p>'\
          '  <p><a href="/return">Back to service</a></p>'\
          '</body>'\
          '</html>'
      else:
        return \
          '<html><head><title>Make Payment</title></head>'\
          '<body style=\"font-size: 150%;\">'\
          '  <h1>GOV.UK Pay</h1>'\
          '  <h2>Enter Your Card Details</h2>'\
          '  <p>Your payment failed. Please return to the service to try again.</p>'\
          '  <p><a href="/return">Back to service</a></p>'\
          '</body>'\
          '</html>'
    elif payments[id]['entered_card']:
      if payments[id]['success']:
        return \
          '<html><head><title>Make Payment </title></head>'\
          '<body style=\"font-size: 150%;\">'\
          '  <h1>GOV.UK Pay</h1>'\
          '  <h2>Enter Your Card Details</h2>'\
          '  <p>You already submitted your details.</p>'\
          '  <p><a href="' + url_for('confirm_get', id=id) + '">Confirm</a></p>'\
          '</body>'\
          '</html>'
      else:
        return \
          '<html><head><title>Make Payment</title></head>'\
          '<body style=\"font-size: 150%;\">'\
          '  <h1>GOV.UK Pay</h1>'\
          '  <h2>Enter Your Card Details</h2>'\
          '  <p>Your payment failed. Please return to the service to try again.</p>'\
          '  <p><a href="/return">Back to service</a></p>'\
          '</body>'\
          '</html>'
    else:
      return \
        '<html><head><title>Make Payment</title></head>'\
        '<body style=\"font-size: 150%;\">'\
        '  <h1>GOV.UK Pay</h1>'\
        '  <h2>Enter Your Card Details</h2>'\
        '  <form action="' + url_for('details_post', id=id) + '" method="POST">'\
        '    <p><select name="card">'\
        '      <option value="valid">4242 4242 4242 4242 (valid)</option>'\
        '      <option value="invalid">9999 9999 9999 9999 (invalid)</option></select></p>'\
        '    <p><button type="submit">Make Payment</button></p></form>'\
        '  </form>'\
        '</body>'\
        '</html>'
    
@app.route('/details/<int:id>', methods=['POST'])
def details_post(id):
    global payments
    
    payments[id]['entered_card'] = True
    
    card = request.form['card']
    if card == 'valid':
      payments[id]['success'] = True
    else:
      payments[id]['success'] = False
    
    return redirect(url_for('confirm_get', id=id), code=303)
  
@app.route('/confirm/<int:id>', methods=['GET'])
def confirm_get(id):
    global payments
    
    if payments[id]['confirmed']:
      if payments[id]['success']:
        return \
          '<html><head><title>Make Payment</title></head>'\
          '<body style=\"font-size: 150%;\">'\
          '  <h1>GOV.UK Pay</h1>'\
          '  <h2>Confirm Payment</h2>'\
          '  <p>You already confirmed this payment and paid successfully. Go back to the service.</p>'\
          '  <p><a href="/return">Back to service</a></p>'\
          '</body>'\
          '</html>'
      else:
        return \
          '<html><head><title>Make Payment</title></head>'\
          '<body style=\"font-size: 150%;\">'\
          '  <h1>GOV.UK Pay</h1>'\
          '  <h2>Confirm Payment</h2>'\
          '  <p>You failed to pay. Go back to the service to try again.</p>'\
          '  <p><a href="/return">Back to service</a></p>'\
          '</body>'\
          '</html>'
    elif payments[id]['success']:
      return '<html><head><title>Confirm Payment</title></head>'\
        '<body style=\"font-size: 150%;\">'\
        '  <h1>GOV.UK Pay</h1>'\
        '  <h2>Confirm Payment</h2>'\
        '  <form action="' + url_for('confirm_post', id=id) + '" method="POST">'\
        '    <p>You really want to pay?</p>'\
        '    <p><button type="submit">Confirm</button></p>'\
        '  </form>'\
        '</body>'\
        '</html>'
    else:
      return '<html><head><title>Confirm Payment</title></head>'\
        '<body style=\"font-size: 150%;\">'\
        '  <h1>GOV.UK Pay</h1>'\
        '  <h2>Confirm Payment</h2>'\
        '  <form action="' + url_for('confirm_post', id=id) + '" method="POST">'\
        '    <p>Your card details were naff.</p>'\
        '    <p><button type="submit">I\'m so sorry</button></p>'\
        '  </form>'\
        '</body>'\
        '</html>'
    
@app.route('/confirm/<int:id>', methods=['POST'])
def confirm_post(id):
  global payments
  payments[id]['confirmed'] = True
  return return_redirect()

@app.route('/return', methods=['GET'])
def return_redirect():
  global DEMO_APP_URL
  print DEMO_APP_URL + 'return'
  return redirect(DEMO_APP_URL + 'return', code=303)

@app.route('/status/<int:id>', methods=['GET'])
def get_status(id):
  global payments
  if id in payments:
    return jsonify(payments[id])
  else:
    return jsonify({ 'found': False })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)