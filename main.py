import os
import logging

import vk_api.bot_longpoll

import functions
import credentials

os.environ["CONFIG_FILE"] = "config.json"
os.environ["ROLES_FILE"] = "roles.json"


def main():
    functions.initialize_database_session()
    vk_session, vk_upload, vk_long_poll = functions.get_vk_connection()
    roles_configuration = functions.get_roles_configuration()
    admins_ids = functions.get_admins_ids_from_config(roles_configuration)
    for event in vk_long_poll.listen():
        event: vk_api.bot_longpoll.VkBotEvent
        bot_event_types = vk_api.bot_longpoll.VkBotEventType
        if event.type == bot_event_types.MESSAGE_NEW:
            event_user_id = event.obj.message["from_id"]
            if event_user_id not in admins_ids:
                print(f"User [{event_user_id}] not admin, skipping...")
                continue
            print(f"User [{event_user_id}] is admin")
            event_user_message = event.obj.message["text"].strip()
            functions.vk_send_message(vk_session, event_user_id, message=event_user_message)
            print(f"Send message to [{event_user_id}] [{event_user_message}]")


if __name__ == '__main__':
    main()
