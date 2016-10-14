from flask import Flask, request, send_file, url_for, render_template, Response
import os
import platform
import glob
import collections
import sys
import re
import mimetypes
app = Flask(__name__)


runpath = os.getcwd()

@app.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response


def send_file_partial(path):
    """ 
        Simple wrapper around send_file which handles HTTP 206 Partial Content
        (byte ranges)
        TODO: handle all send_file args, mirror send_file's error handling
        (if it has any)
    """
    range_header = request.headers.get('Range', None)
    if not range_header: return send_file(path)
    
    size = os.path.getsize(path)    
    byte1, byte2 = 0, None
    
    m = re.search('(\d+)-(\d*)', range_header)
    g = m.groups()
    
    if g[0]: byte1 = int(g[0])
    if g[1]: byte2 = int(g[1])

    length = size - byte1
    if byte2 is not None:
        length = byte2 - byte1
    
    data = None
    with open(path, 'rb') as f:
        f.seek(byte1)
        data = f.read(length)

    rv = Response(data, 
        206,
        mimetype=mimetypes.guess_type(path)[0], 
        direct_passthrough=True)
    rv.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(byte1, byte1 + length - 1, size))

    return rv

@app.route("/1/<path:f>")
def p1(f):
  is os.path.isdir(f):
    return showdir(f)
  return send_file_partial("/projects/grail/supasorn/" + f);

@app.route("/2nb/<path:f>")
def p2(f):
  is os.path.isdir(f):
    return showdir(f)
  return send_file_partial("/projects/grail/supasorn2nb/" + f);

@app.route("/home/<path:f>")
def p3(f):
  is os.path.isdir(f):
    return showdir(f)
  return send_file_partial("/homes/grail/supasorn/" + f);

def showdir(p):
  fs = sorted(os.listdir(p))
  st = ""
  for f in fs:
    st += "<a href='/here/" + p + "/" + f + "'>" + f + "</a><br/>"
  return st

@app.route("/here/<path:f>")
def here(f):
  if os.path.isdir(f):
    return showdir(f)
  return send_file_partial(runpath + "/" + f);

@app.route("/here/")
def here2():
  return showdir('.') 

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=5050)

