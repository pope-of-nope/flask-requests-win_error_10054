# flask-requests-win_error_10054

## DO YOU CARE ABOUT THIS REPO?
Probably not, unless the following are all true:
- You're getting a "requests.exceptions.ConnectionError" with the code 10054 ('An existing connection was forcibly closed by the remote host')
- You're writing a server in "flask", and you've got client code written in python using the "requests" library (such as your tests.)
- The problem is endpoint specific (some are fine, others aren't.)
- The problem never occurs with a GET request--only on some/all of your POST, PUT or DELETE requests.

## STILL READING?
If that sounds like you, then clone this repo and try running the server/tests under "example":
-  python ./example/server.py  # run the server first
-  python ./example/tests.py  # the run the tests

If you see any tests "FAIL" then this is the repository you're looking for.

## WHY IS THIS HAPPENING?
If your flask route returns a response without reading the request body, the client-side connectino blows up.
I created this repository to bypass second-guessing. This is simply what I'm observing, and I'm not trying to blame anyone's library.
I've been using requests/flask for over a year now, and ran into this issue quite suddenly. (I lost 2 days because I trusted they weren't the problem.)

## HOW DO I FIX IT.
"workaround.py" contains two options. 
- "global_hotfix" contains an example how to fix the issue for every route (using an "@app.before_request" decorator.)
- "route-hotfix" contains an example how to fix the issue for individual routes (using a "@hotfix" decorator after your "@app.route(...)" decorator.)

Probably not. The error is environment specific. 
  The error (keywords):
    - An existing connection was forcibly closed by the remote host.
    - WinError 10054

  My environment:
  - Windows 7
  - Python 3.6.2
  - Requests 2.18.4
  - Flask 0.12.2

If you're using those libraries, you can test 
But you can test it by running the following code.
  python ./example/server.py  # run the server first
  python ./example/tests.py  # the run the tests

If you see "FAIL" in those tests, congratulations! This project has the solution to your WinError 10054.
I
If you've run into the WinError 10054 
I ran into a very strange bug 
