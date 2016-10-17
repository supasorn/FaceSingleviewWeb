from flask import Flask, request, send_file, url_for, render_template, Response
import os
import platform
import glob
import collections
import sys
import re
import mimetypes
import json
from collections import OrderedDict
app = Flask(__name__)


runpath = os.getcwd()
history = "/projects/grail/supasorn/face-singleview/web/history.txt"

@app.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response

def saveHistory(path):
  with open(history, "r") as fi:
    lines = fi.readlines()

  fo = open(history, "w")
  fo.write(path + "\n")
  for line in lines:
    if line.strip() != path:
      fo.write(line)
  fo.close()

def send_file_partial(path):
  saveHistory(path)
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

def display(f):
  if os.path.isdir(f):
    return showdir(f)
  return send_file_partial(f);

def showdir(p):
  fs = sorted(os.listdir(p))
  st = ""
  for f in fs:
    #st += "<a href='/here/" + p + "/" + f + "'>" + f + "</a><br/>"
    if os.path.isdir(p + "/" + f):
      st += "<a href='" + f + "/'>" + f + "/</a><br/>"
    else:
      st += "<a href='" + f + "'>" + f + "</a><br/>"

  return st

def printTree(tree, tab, path):
  if tree == "Leaf":
    return ""
  output = ""
  leaves = 0
  leaflim = 10
  for key in tree:
    t = tree
    k = key
    p = path

    output2 = ""
    while isinstance(t[k], dict) and len(t[k]) == 1:
      p += "/" + k
      output2 += k + "/"
      t = t[k]
      k = t.iterkeys().next()
    p += "/" + k
    if t[k] == "Leaf":
      if leaves < leaflim:
        output2 += k
        output += ("&nbsp;" * tab * 5) + "<a href='" + p + "'>" + output2 + "</a><br>"
      elif leaves == leaflim:
        output2 += k
        output += ("&nbsp;" * tab * 5) + "...<br/>"
      else:
        None
      leaves += 1
    else:
      output2 += k 
      output += ("&nbsp;" * tab * 5) + "<a style='color: black; font-size: 20px;' href='" + p + "/'>" + output2 + "/</a><br>" + printTree(t[k], tab+1, p)


  return output



@app.route("/")
def root():
  with open(history) as f:
    lines = f.readlines()
  root = OrderedDict()

  
  output = ""
  for line in lines:
    cur = root
    st = line.strip().split("/")
    output += "<a href='" + line.strip() + "'>" + line.strip() + "</a><br>"
    for i in range(len(st)):
      s = st[i]
      if s == "": continue
      if s not in cur:
        if i == len(st) - 1:
          cur[s] = "Leaf"
        else:
          cur[s] = OrderedDict()
      cur = cur[s]

  #output += json.dumps(root)
  #output = "<p style='font-family: courier new;'>" + printTree(root, 0) + "</p>"

  return '<style>a { text-decoration: none; color: blue; }</style><div style="width: 100%;overflow:auto"><div style="float:left; width: 50%">' + printTree(root, 0, "") + '</div><div style="float:right; width: 50%">' + output + '</div></div>'
    


#@app.route("/1/<path:f>/")
#def p1(f):
  #print f
  #return display("/projects/grail/supasorn/" + f)

#@app.route("/2nb/<path:f>/")
#def p2(f):
  #return display("/projects/grail/supasorn2nb/" + f)

#@app.route("/home/<path:f>/")
#def p3(f):
  #return display("/homes/grail/supasorn/" + f)

@app.route("/<path:f>/")
def p(f):
  return display("/" + f)

@app.route("/here/<path:f>/")
def here(f):
  if os.path.isdir(f):
    return showdir(f)
  return send_file_partial(runpath + "/" + f);

@app.route("/here/")
def here2():
  return showdir('.') 


if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=5050)

