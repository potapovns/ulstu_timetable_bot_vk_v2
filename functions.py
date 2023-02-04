import os
import json

import vk_api

from data import db_session


def get_configuration_from_file(config_filename):
    with open(config_filename) as file:
        config_json = json.load(file)
    return config_json


def get_database_connection_config(configuration, database_username, database_password):
    db_config = configuration["database_config"]
    db_config["username"] = database_username
    db_config["password"] = database_password
    return db_config


def get_database_credentials():
    username = os.environ.get("DATABASE_USERNAME", None)
    password = os.environ.get("DATABASE_PASSWORD", None)
    return username, password


def get_config_filename():
    config_filename = os.environ.get("CONFIG_FILE", None)
    return config_filename


def initialize_database_session():
    config_filename = get_config_filename()
    db_config = get_configuration_from_file(config_filename)
    db_username, db_password = get_database_credentials()
    db_connection_config = get_database_connection_config(
        db_config,
        db_username,
        db_password
    )
    db_session.global_init(db_connection_config)


def get_vk_token():
    vk_token = os.environ.get("VK_TOKEN", None)
    return vk_token


def get_vk_session():
    vk_token = get_vk_token()
    vk_session = vk_api.VkApi(token=vk_token)
    return vk_session


def get_vk_group_id():
    vk_group_id = os.environ.get("VK_GROUP_ID", None)
    return vk_group_id


def get_vk_upload(vk_session):
    vk_upload = vk_api.VkUpload(vk_session)
    return vk_upload


def get_vk_long_poll(vk_session, group_id):
    vk_long_poll = vk_api.bot_longpoll.VkBotLongPoll(vk_session, group_id)
    return vk_long_poll


def get_vk_connection():
    vk_session = get_vk_session()
    vk_group_id = get_vk_group_id()
    vk_upload = get_vk_upload(vk_session)
    vk_long_poll = get_vk_long_poll(vk_session, vk_group_id)
    return vk_upload, vk_upload, vk_long_poll
