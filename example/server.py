from flask import Flask, jsonify, request, Response, abort
from functools import wraps
from werkzeug.exceptions import HTTPException


app = Flask('app')


@app.route("/fubar/error/<int:code>", methods=["GET", "POST"])
def fubar_error(code):
    if 400 <= code <= 599:
        if request.method == 'GET':
            return abort(code)  # works.
        elif request.method == "POST":
            abort(code)  # won't work. even if you use middleware to catch errors.
    else:
        raise ValueError("invalid error code.")


@app.route("/working/error/<int:code>", methods=["GET", "POST"])
def working_error(code):
    if 400 <= code <= 599:
        if request.method == 'GET':
            return abort(code)  # continues to work.
        elif request.method == "POST":
            trash_it = request.json  # this is the only thing that suffices to solve the problem.
            print(trash_it)
            abort(code)  # this will work (now that we've read the request body.)
    else:
        raise ValueError("invalid error code.")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
