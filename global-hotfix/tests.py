import requests
import flask
from functools import wraps


def error_filter(e):
    """ we only want to catch the Win Error 10054. """
    if not isinstance(e, requests.exceptions.ConnectionError):
        return False
    else:
        try:
            if e.args[0].args[1].args[0] == 10054:
                return True
            else:
                return False
        except:
            return False


def assert_true(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            if isinstance(result, bool) and result:
                print("pass. should/did: True")
            else:
                print("FAIL. should: True, did: False)")
            return result
        except Exception as e:
            print("FAIL. should: True, did: ", e)
            return e

    return decorated


def assert_10054_error(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            print("FAIL. should: 10054 error, did: ", result)
        except Exception as e:
            if error_filter(e):
                print("pass. should/did: ", e)
            else:
                print("FAIL. should: 10054 error, did: ", e)
            return e

    return decorated


if flask.__version__ != '0.12.2':
    print("note: you're using a different version of 'flask' than is in the requirements.txt file.")


if requests.__version__ != '2.18.4':
    print("note: you're using a different version of 'requests' than is in the requirements.txt file.")


def make_url(path):
    """ This is a terrible function. Don't take it as a reference in your own code.
    It just happens to be good enough for our purposes here. """
    return "http://localhost:5000/{path}".format(path=path)


def fubar_error_url(code):
    return make_url("fubar/error/{code}".format(code=code))


def working_error_url(code):
    return make_url("working/error/{code}".format(code=code))


def why_it_matters_url():
    return make_url("fubar/auth")


def run_tests():
    def run_fubar_error_tests():
        @assert_true
        def run_get_test(code):
            """ this issue should never occur with GET requests. """
            url = fubar_error_url(code)
            print("\nGET ", url)
            res = requests.get(url)
            return res.status_code == code

        @assert_true
        def run_post_test(code):
            """ if the server doesn't read "request.json()" then the issue occurs. """
            url = fubar_error_url(code)
            print("\nPOST ", url)
            res = requests.post(url, json={"doesn't": "matter"})
            return res.status_code == code

        run_get_test(400)
        run_get_test(401)
        run_get_test(404)
        run_get_test(405)
        run_get_test(409)

        run_post_test(400)
        run_post_test(401)
        run_post_test(404)
        run_post_test(405)
        run_post_test(409)

    def run_working_error_tests():
        @assert_true
        def run_get_test(code):
            """ this issue should never occur with GET requests. """
            url = working_error_url(code)
            print("\nGET ", url)
            res = requests.get(url)
            return res.status_code == code

        @assert_true
        def run_post_test(code):
            """ if the server reads "request.json()" then the issue goes away. """
            url = working_error_url(code)
            print("\nPOST ", url)
            res = requests.post(url, json={"doesn't": "matter"})
            return res.status_code == code

        run_get_test(400)
        run_get_test(401)
        run_get_test(404)
        run_get_test(405)
        run_get_test(409)

        run_post_test(400)
        run_post_test(401)
        run_post_test(404)
        run_post_test(405)
        run_post_test(409)

    def run_why_it_matters_tests():
        def run_authorized():
            @assert_true
            def run_get_test():
                """ this issue should never occur with GET requests. """
                url = why_it_matters_url()
                print("\nGET ", url)
                res = requests.get(url, auth=('username', 'password'))
                return res.status_code == 200

            @assert_true
            def run_post_test():
                url = why_it_matters_url()
                print("\nPOST ", url)
                res = requests.post(url, json={"doesn't": "matter"}, auth=('username', 'password'))
                # print(res.json())
                return res.status_code == 200

            run_get_test()
            run_post_test()

        def run_anonymous():
            @assert_true
            def run_get_test():
                """ this issue should never occur with GET requests. """
                url = why_it_matters_url()
                print("\nGET ", url)
                res = requests.get(url)
                return res.status_code == 401

            @assert_true
            def run_post_test():
                """ this is another Win Error : ( """
                url = why_it_matters_url()
                print("\nPOST ", url)
                res = requests.post(url, json={"doesn't": "matter"})
                # print(res.json())
                return res.status_code == 401

            run_get_test()
            run_post_test()

        run_authorized()
        run_anonymous()

    run_fubar_error_tests()
    run_working_error_tests()
    run_why_it_matters_tests()

if __name__ == '__main__':
    run_tests()
