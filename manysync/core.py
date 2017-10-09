import os
import webbrowser
import json

from boxsdk import OAuth2, Client
from boxsdk.exception import BoxOAuthException

from . import server
from . import config as cfg

CONFIG_FILE = os.path.join(os.getcwd(), "config.json")
configuration = cfg.Config()


def sanitize_config_line(line):
    """
        sanitizes the configuration entries
    :param line:
        line from configuration file
    :return:
        sanitized config parameter
    """
    return line.replace("\n", "")


authorization_token = None


def store_auth_token(code):
    global authorization_token
    authorization_token = code


def show_folder(folder_id='0', client=None):
    if client is not None:
        root_folder = client.folder(folder_id=folder_id).get()
        for item in root_folder.get_items(100):
            print("Type: {0} - ID: {1} - Name: {2}".format(item.id, item.type, item.name))
    else:
        print("Client is none")


def connect(config):
    """
    connects to box.com
    :param config: a loaded instance of Config
    :return: a boxsdk.Client instance
    """
    oauth = OAuth2(client_id=config.client_id, client_secret=config.client_secret,
                   access_token=config.access_token, refresh_token=config.refresh_token)
    return Client(oauth)


def authenticate(config):
    oauth = OAuth2(client_id=config.client_id, client_secret=config.client_secret)
    auth_url, csrf_token = oauth.get_authorization_url("http://localhost:9010")
    server.store_auth_token = store_auth_token
    webbrowser.open(auth_url)
    server.start()
    print("passed code is ", authorization_token)
    access_token, refresh_token = oauth.authenticate(authorization_token)
    config.access_token = access_token
    config.refresh_token = refresh_token
    cfg.save_config(config, CONFIG_FILE)


def main():
    print("Entering core.main")
    global configuration
    global CONFIG_FILE
    cfg.load_config(configuration, CONFIG_FILE)

    if configuration.access_token is None or configuration.refresh_token is None:
        authenticate(configuration)

    #try to connect
    print("connecting")
    client = connect(configuration)
    print("connected")
    oauth = OAuth2(client_id=configuration.client_id, client_secret=configuration.client_secret,
                   access_token=configuration.access_token, refresh_token=configuration.refresh_token)

    cfg.save_config(configuration, CONFIG_FILE)

    client = Client(oauth)

    try:
        show_folder('0', client)
    except BoxOAuthException:
        refreshed_access_token = oauth.refresh(configuration["authorization_token"])
        configuration["authorization_token"] = refreshed_access_token[0]
        configuration["refresh_token"] = refreshed_access_token[1]
        client = Client(oauth)
