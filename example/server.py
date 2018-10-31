from flask import Flask, jsonify, request, Response, abort
import time


app = Flask('app')


@app.errorhandler(401)
def unauthorized(e):
    return jsonify({"message": "Not Authorized"}), 401


@app.route("/fubar/error/<int:code>", methods=["GET", "POST"])
def fubar_error(code):
    """ example of the issue. (GET works; POST does not.) """
    if 400 <= code <= 599:
        if request.method == 'GET':
            return abort(code)  # works.
        elif request.method == "POST":
            abort(code)  # won't work. even if you use middleware to catch errors.
    else:
        raise ValueError("invalid error code.")


@app.route("/working/error/<int:code>", methods=["GET", "POST"])
def working_error(code):
    """ example of how to fix the issue. (GET works; POST does too.) """
    if 400 <= code <= 599:
        if request.method == 'GET':
            return abort(code)  # continues to work.
        elif request.method == "POST":
            somehow_this_fixes_it = request.json  # this is the only thing that suffices to solve the problem.
            abort(code)  # this will work (now that we've read the request body.)
    else:
        raise ValueError("invalid error code.")


# the above two examples are sufficient to demonstrate the issue.
# what follows are more examples.
@app.route("/fubar/auth", methods=["GET", "POST"])
def why_does_the_issue_matter():
    """ reasonable ask: I shouldn't be forced to read the body of an unauthorized request.
    problem: if I abort a request with a body, I've just ensured a WinError 10054 for some of my users.
    """
    def request_is_authorized():
        auth = request.authorization
        if auth:
            username = auth.username
            password = auth.password
            print(username, password)
            return True
        else:
            return False

    if request_is_authorized():
        print(request.json)
        body = jsonify({"now": int(time.time())})
        return body, 200
    else:
        print("not authorized!")
        abort(401)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
