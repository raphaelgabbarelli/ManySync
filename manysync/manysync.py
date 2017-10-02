import os
import webbrowser
from boxsdk import OAuth2, Client
from boxsdk.exception import BoxOAuthException
import server
import json

import config as cfg

CONFIG_FILE = os.path.join(os.getcwd(), "config .json")

configuration = cfg.Config()

cfg.load_config(configuration, CONFIG_FILE)
print(configuration.client_id)

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
    configuration["authorization_token"] = code


def save_access_token(authorization_code, refresh_code):
    auth_file = open(auth_token_file_path, "w")
    auth_file.write(authorization_code + "\n")
    auth_file.write(refresh_code)
    auth_file.close()



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
            configuration["client_id"] = sanitize_config_line(line)
        elif line_number == 2:
            configuration["client_secret"] = sanitize_config_line(line)
        line_number += 1
    config_file.close()


# if we already have an authorization token, we should try to use it!
if os.path.isfile(auth_token_file_path):
    print("Loading access/refresh token")
    auth_file = open(auth_token_file_path)
    configuration.access_token = sanitize_config_line(auth_file.readline())
    configuration.refresh_token = sanitize_config_line(auth_file.readline())
    auth_file.close()

if configuration["authorization_token"] is None:
    oauth = OAuth2(client_id=configuration.client_id, client_secret=configuration.client_secret)
    auth_url, csrf_token = oauth.get_authorization_url("http://localhost:9010")
    server.store_auth_token = store_auth_token
    webbrowser.open(auth_url)
    server.start()
    oauth = OAuth2(client_id=configuration.client_id, client_secret=configuration.client_secret)
    authorization_token, refresh_token = oauth.authenticate(configuration.authorization_token)
    save_access_token(authorization_token, refresh_token)


oauth = OAuth2(client_id=configuration["client_id"], client_secret=configuration["client_secret"], access_token=configuration["authorization_token"], refresh_token=configuration["refresh_token"])

with open("config.json", "w") as f:
    json.dump(configuration, f)

client = Client(oauth)


def show_folder(folder_id='0', client=None):
    if client is not None:
        root_folder = client.folder(folder_id=folder_id).get()
        for item in root_folder.get_items(100):
            print("Type: {0} - ID: {1} - Name: {2}".format(item.id, item.type, item.name))
    else:
        print("Client is none")

try:
    show_folder('0', client)
except BoxOAuthException:
    refreshed_access_token = oauth.refresh(configuration["authorization_token"])
    configuration["authorization_token"] = refreshed_access_token[0]
    configuration["refresh_token"] = refreshed_access_token[1]
    client = Client(oauth)