import flask

app = flask.Flask(__name__)


# this is supposed to be overridden by the client code
def store_auth_token(code):
    pass


def start():
    app.run(port=9010)


def kill():
    func = flask.request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError("not running werkzeug server")
    func()


@app.route("/", methods=["GET"])
def token():
    code = flask.request.args["code"]
    store_auth_token(code)
    kill()
    return "code stored!"


if __name__ == "__main__":
    start()
