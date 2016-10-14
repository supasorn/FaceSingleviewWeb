from flask import Flask, request, send_file, url_for, render_template, Response
import os
import platform
import glob
import collections
import re
import mimetypes
app = Flask(__name__)

if platform.dist()[0] == 'fedora':
    data = "/projects/grail/supasorn/face-singleview/data/"
else:
    data = "/home/supasorn/face-singleview/data/"

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

@app.route("/<guy>/<movie>/update", methods=['POST'])
def update(guy, movie):
    f = open(data + "/" + guy + "/" + movie + "/probeselect.txt", "w")
    f.write(request.form["data"])
    f.close()
    return "1"

@app.route("/imgs/<path:p>")
def c(p):
    if p[-3:] == "jpg" and os.path.exists(data + "/" + p):
        return send_file(data + "/" + p)
    return ('invalid', 403)

@app.route("/video/<path:p>")
def video(p):
    if p[-3:] in ["mp4", "avi"] and os.path.exists(data + "/" + p):
        return send_file_partial(data + "/" + p)

@app.route("/<guy>/<movie>/result")
def result(guy, movie):
    lst = os.listdir(data + "/" + guy)
    print "-----------------"
    print lst
    videos = []
    for f in sorted(lst):
        if movie + "_" in f and os.path.isdir(data + "/" + guy + "/" + f):
            if not os.path.exists(data + "/" + guy + "/" + f + "/origImgs/0001.png"): continue
            if os.path.exists(data + "/" + guy + "/" + f + "/text_sound.mp4"):
                videos.append({"name": f, "url": "/video/" + guy + "/" + f + "/text_sound.mp4"})
            elif os.path.exists(data + "/" + guy + "/" + f + "/puppet_sound.mp4"):
                videos.append({"name": f, "url": "/video/" + guy + "/" + f + "/puppet_sound.mp4"})
            elif os.path.exists(data + "/" + guy + "/" + f + "/shading.mp4"):
                videos.append({"name": f, "url": "/video/" + guy + "/" + f + "/shading.mp4"})
    return render_template("showvideo.html", videos=videos)
    #return ('invalid', 403)

@app.route("/<guy>/<movie>/", methods=['GET', 'POST'])
def pick(guy, movie):
    #print dict(request.args.items())
    st = ""
    count = 0

    mp = collections.defaultdict(lambda: 0)
    if os.path.exists(data + "/" + guy + "/" + movie + "/probeselect.txt"):
        f = open(data + "/" + guy + "/" + movie + "/probeselect.txt", "r").readlines()
        for x in f:
            v = x.strip().split(" ")
            mp[v[0]] = v[1]

    for f in sorted(os.listdir(data + "/" + guy + "/" + movie + "/probe")):
        #if count % 10 == 0:
            #st += "<br/>"
        st += "<img id='" + f + "' class='clickable " + ("no" if mp[f] == "0" else "") + "' src='../../imgs/" + guy + "/" + movie + "/probe/" + f + "' width='100'/>"
        count += 1
    return render_template("template.html", imgs=st) 

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5432)
