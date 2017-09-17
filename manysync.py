import os
import flask
import webbrowser
from boxsdk import OAuth2, Client


def sanitize_config_line(line):
    """
        sanitizes the configuration entries
    :param line:
        line from configuration file
    :return:
        sanitized config parameter
    """
    return line.replace("\n", "")


config = {"client_id": None, "client_secret": None}
config_file_path = os.path.join(os.getcwd(), "config.txt")
auth_token_file_path = os.path.join(os.getcwd(), "auth.txt")

if not os.path.isfile(config_file_path):
    print("Config file not found")
    pass
else:
    print("Loading config...")
    config_file = open(config_file_path)
    line_number = 1
    for line in config_file:
        if line_number == 1:
            config["client_id"] = sanitize_config_line(line)
        elif line_number == 2:
            config["client_secret"] = sanitize_config_line(line)
        line_number += 1

oauth = OAuth2(client_id=config["client_id"], client_secret=config["client_secret"])
auth_url, csrf_token = oauth.get_authorization_url("http://localhost:9010")
webbrowser.open(auth_url)


def store_auth_token(code):
    auth_file = open(auth_token_file_path, "w")
    auth_file.write(code)


app = flask.Flask(__name__)
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
    app.run(port=9010)
