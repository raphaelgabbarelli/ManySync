import os
import webbrowser
from boxsdk import OAuth2, Client
import server

def sanitize_config_line(line):
    """
        sanitizes the configuration entries
    :param line:
        line from configuration file
    :return:
        sanitized config parameter
    """
    return line.replace("\n", "")


def store_auth_token(code):
    config["authorization_token"] = code


def save_access_token(code):
    auth_file = open(auth_token_file_path, "w")
    auth_file.write(code)
    auth_file.close()


config = {"client_id": None, "client_secret": None, "access_token": None, "authorization_token": None}
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
    config_file.close()


# if we already have an authorization token, we should try to use it!
if os.path.isfile(auth_token_file_path):
    print("Loading access token")
    auth_file = open(auth_token_file_path)
    config["access_token"] = sanitize_config_line(auth_file.readline())
    auth_file.close()

if config["access_token"] is None:
    oauth = OAuth2(client_id=config["client_id"], client_secret=config["client_secret"])
    auth_url, csrf_token = oauth.get_authorization_url("http://localhost:9010")
    server.store_auth_token = store_auth_token
    webbrowser.open(auth_url)
    server.start()
    oauth = OAuth2(client_id=config["client_id"], client_secret=config["client_secret"])
    access_token, refresh_token = oauth.authenticate(config["authorization_token"])
    save_access_token(access_token)


oauth = OAuth2(client_id=config["client_id"], client_secret=config["client_secret"], access_token=config["access_token"])
client = Client(oauth)
root_folder = client.folder(folder_id='0').get()
for key in root_folder.keys():
    print(key + " " + root_folder[key])
