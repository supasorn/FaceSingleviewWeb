from flask import Flask, request, send_file, url_for, render_template
import os
import platform
import glob
import collections
app = Flask(__name__)

@app.route("/<path:f>")
def update(f):
    return send_file("/projects/grail/supasorn/face-singleview/data/" + f);

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5050)
