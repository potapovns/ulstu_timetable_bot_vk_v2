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


def get_roles_filename():
    roles_filename = os.environ.get("ROLES_FILE", None)
    return roles_filename


def get_roles_config_from_file(roles_filename):
    with open(roles_filename) as file:
        roles_json = json.load(file)
    return roles_json


def get_admins_ids_from_config(roles_configuration):
    admins_ids = roles_configuration["admin"]
    return admins_ids


def get_roles_configuration():
    roles_filename = get_roles_filename()
    roles_config = get_roles_config_from_file(roles_filename)
    return roles_config


def vk_send_message(vk_session, user_id, message=None, keyboard=None, pic_name=None):
    if message is None:
        message = ""
    post = {
        'user_id': user_id,
        'message': message,
        # 'random_id': random.randint(0, 2 ** 64),
    }
    if pic_name is not None:
        post['attachment'] = pic_name
    if keyboard is not None:
        post['keyboard'] = keyboard.get_keyboard()
    vk_session.method('messages.send', post)
