from flask import Flask
import urllib2
import requests
import json
import time
from flask import Response, stream_with_context
from flask import render_template, redirect, render_template_string


app = Flask(__name__)
@app.route("/")
def index():

  return render_template("index.html")

if __name__ == '__main__': 
  app.run(host="0.0.0.0", port=8080) 