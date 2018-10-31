import requests
import flask
from functools import wraps


def test_case(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        result = f(*args, **kwargs)
        if not isinstance(result, bool):
            raise TypeError(result)
        else:
            print("test result: ", result)
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


def run_tests():
    def run_fubar_error_tests():
        @test_case
        def run_get_test(code):
            url = fubar_error_url(code)
            res = requests.get(url)
            return res.status_code == code

        @test_case
        def run_post_test(code):
            url = fubar_error_url(code)
            res = requests.post(url, json={"doesn't": "matter"})
            return res.status_code == code

        run_get_test(400)
        run_get_test(401)
        run_get_test(404)
        run_get_test(409)
        run_get_test(405)


    run_fubar_error_tests()

if __name__ == '__main__':
    run_tests()
