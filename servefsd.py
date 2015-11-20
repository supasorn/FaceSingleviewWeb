from flask import Flask, request, send_file, url_for, render_template
import os
import platform
import glob
import collections
app = Flask(__name__)

data = "/projects/grail/supasorn/face-reconstruction-pipeline/data/"
@app.route("/video/<path:p>")
def video(p):
    if p[-3:] == "mp4" and os.path.exists(data + "/" + p):
        return send_file(data + "/" + p)

@app.route("/<guy>/<movie>/result")
def result(guy, movie):
    lst = os.listdir(data + "/" + guy)
    print "-----------------"
    print lst
    videos = []
    for f in sorted(lst):
        if movie + "_" in f and os.path.isdir(data + "/" + guy + "/" + f):
            if os.path.exists(data + "/" + guy + "/" + f + "/text_sound.mp4"):
                videos.append({"name": f, "url": "/video/" + guy + "/" + f + "/text_sound.mp4"})
    return render_template("showvideo.html", videos=videos)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5050)
