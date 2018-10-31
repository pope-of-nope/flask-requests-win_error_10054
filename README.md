# flask-requests-win_error_10054

## DO YOU CARE ABOUT THIS REPO?
Probably not, unless the following are all true:
- You're getting a "requests.exceptions.ConnectionError" with the code 10054 ('An existing connection was forcibly closed by the remote host')
- You're writing a server in "flask", and you've got client code written in python using the "requests" library (such as your tests.)
- The problem is endpoint specific (some are fine, others aren't.)
- The problem never occurs with a GET request--only on some/all of your POST, PUT or DELETE requests.

## STILL READING?
If that sounds like you, then clone this repo and try running the server/tests under "example":
-  python ./example/server.py  # first, run the server
-  python ./example/tests.py  # next, run the tests

If you see any tests "FAIL" then this is the repository you're looking for.

## WHY IS THIS HAPPENING?
The client's connection blows up if it sends a request body but the server ignores the body. This is specifically something in how Flask and Requests interact (either directly or by some deeper interaction of their dependencies.) 

The issue disappears if you send the request from another client (for example, Postman worked just fine for me.)

I don't know why these libraries work this way. But I do know that you can work around the issue by reading the request body. (This workaround isn't ideal--see "why this is a problem.")

## HOW DO I FIX IT.
"workaround.py" contains two options. 
- the "global-hotfix" directory contains an example how to fix the issue for every route (using an "@app.before_request" decorator.)
- the "route-hotfix" directory contains an example how to fix the issue for individual routes (using a "@hotfix" decorator after your "@app.route(...)" decorator.)

## WHY IS THIS A PROBLEM?
OR: WHAT LEGITIMATE USE CASE IS THERE FOR IGNORING THE BODY OF A POST, PUT OR DELETE REQUEST?

Here's the one I ran into: adding authorization filters to my flask routes.
- Suppose I write a Flask route that checks the authorization header. If this header is bad, abort the request with a 401 code immediately.
- But wait! If I abort before you read the request body, then I've blown my client's connections!
- And now I'm forced to choose between processing untrusted input vs supporting my test code (which I wrote in python.)

## FINAL NOTES
- I will update this project if I find a better solution.
- I haven't tried replicating the issue on other versions of python, flask or requests.
- This code is provided as-is.
- Use at your own risk.

