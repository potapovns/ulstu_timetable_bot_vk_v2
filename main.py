import os
import logging
import functions
import credentials

os.environ["CONFIG_FILE"] = "config.json"


def main():
    functions.initialize_database_session()
    vk_session, vk_upload, vk_long_poll = functions.get_vk_connection()


if __name__ == '__main__':
    main()
