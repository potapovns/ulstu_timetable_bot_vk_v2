import datetime
import os
import logging

import vk_api.bot_longpoll

import functions
import credentials

os.environ["CONFIG_FILE"] = "config.json"
os.environ["ROLES_FILE"] = "roles.json"

os.environ["LOG_FILENAME"] = "main.log"

BOT_EVENT_TYPES = vk_api.bot_longpoll.VkBotEventType


def main():
    functions.initialize_logging()
    logger = logging.getLogger(__name__)
    logger.info("Logger initialized")
    functions.initialize_database_session()
    vk_session, vk_upload, vk_long_poll = functions.get_vk_connection()
    roles_configuration = functions.get_roles_configuration()
    admins_ids = functions.get_admins_ids_from_config(roles_configuration)
    for event in vk_long_poll.listen():
        logging.debug(f"Get new event: {event.type}")
        if event.type == BOT_EVENT_TYPES.MESSAGE_NEW:
            event_user_id = event.obj.message["from_id"]
            event_user_message = event.obj.message["text"].strip()
            logger.debug(f"New message from [{event_user_id}], message [{event_user_message}]")
            try:
                functions.vk_send_message(vk_session, event_user_id, message=event_user_message)
            except Exception as e:
                logger.error("Exception occurred", exc_info=True)


if __name__ == '__main__':
    main()
