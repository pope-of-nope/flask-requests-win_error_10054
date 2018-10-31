from functools import wraps
from flask import request


def global_hotfix():
    try:
        if request.headers["User-Agent"].startswith('python-requests'):
            if request.method in ["POST", "PUT", "DELETE"]:
                black_magic = request.json
    except Exception as e:
        print(e)
    finally:
        return


def hotfix(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            if request.headers["User-Agent"].startswith('python-requests'):
                if request.method in ["POST", "PUT", "DELETE"]:
                    black_magic = request.json
        except Exception as e:
            print(e)
        finally:
            return f(*args, **kwargs)

    return decorated
