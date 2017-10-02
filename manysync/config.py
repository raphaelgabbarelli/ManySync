import json
import os


class Config:

    def __init__(self):
        __client_id = None
        __client_secret = None
        __access_token = None
        __refresh_token = None

    @property
    def client_id(self):
        return self.__client_id

    @client_id.setter
    def client_id(self, client_id):
        self.__client_id = client_id

    @property
    def client_secret(self):
        return self.__client_secret

    @client_secret.setter
    def client_secret(self, client_secret):
        self.__client_secret = client_secret

    @property
    def access_token(self):
        return self.__access_token

    @access_token.setter
    def access_token(self, access_token):
        self.__access_token = access_token

    @property
    def refresh_token(self):
        return self.__refresh_token

    @refresh_token.setter
    def refresh_token(self, refresh_token):
        self.__refresh_token = refresh_token


def save_config(config, file_path):
    if os.path.isfile(file_path):
        with open(file_path, "w") as f:
            json.dump({"client_id": config.__client_id, "client_secret": config.__client_secret, "access_token": config.__access_token, "refresh_token": config.__refresh_token}, f)


def load_config(config, file_path):
    if os.path.isfile(file_path):
        with open(file_path, "r") as f:
            cfg_dict = json.load(f)
            config.client_id = cfg_dict["client_id"]
            config.client_secret = cfg_dict["client_secret"]
            config.access_token = cfg_dict["access_token"]
            config.refresh_token = cfg_dict["refresh_token"]
