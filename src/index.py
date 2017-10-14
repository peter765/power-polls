from flask import Flask
import requests
import json
import time
from flask import Response, stream_with_context
from flask import render_template, redirect, render_template_string


app = Flask(__name__)
@app.route("/")
def index():
  fakeData = {'one': ['BillOne','2017-05-13','123',456],'two':['BillTwo','2017-03-13','589',654], 'three':['BillThree','2017-02-18','48',13]}
  return render_template("index.html", data=fakeData)

@app.route("/billview/<string:bill_id>", methods=['GET'])
def view_bill_details(bill_id):
  fakeData = {'summary':'summary of infomration will go here','components':['componentid', 'information for compoenent component']}
  return render_template("summary.html", data=fakeData)


if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8000)
