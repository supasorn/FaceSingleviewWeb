from flask import Flask, request, send_file, url_for, render_template
import os
import glob
import collections
app = Flask(__name__)

data = "/home/supasorn/face-singleview/data/"

@app.route("/")
def test():
    print url_for("m.png")
    return "yes"

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

    for f in os.listdir(data + "/" + guy + "/" + movie + "/probe"):
        if count % 10 == 0:
            st += "<br/>"
        st += "<img id='" + f + "' class='clickable " + ("no" if mp[f] == "0" else "") + "' src='../../imgs/" + guy + "/" + movie + "/probe/" + f + "' width='100'/>"
        count += 1
    return render_template("template.html", imgs=st) 

if __name__ == "__main__":
    app.run(debug=True)
