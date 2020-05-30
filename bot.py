import requests
import configparser as cfg


class BotHandler:

    def __init__(self, config):
        self.token = self.read_token(config)
        self.api_url = "https://api.telegram.org/bot{}/".format(self.token)

    def get_updates(self, offset=None, timeout=5):
        response = requests.get(self.api_url + 'getUpdates', {'timeout': timeout, 'offset': offset})
        return response.json()['result']

    def send_message(self, chat_id, text):
        return requests.post(self.api_url + 'sendMessage', {'chat_id': chat_id, 'text': text})

    def read_token(self, config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('credentials', 'token')

    def get_last_update(self):
        get_result = self.get_updates()
        last_update = None
        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = None
        return last_update


text_bot = BotHandler("config.cfg")


def main():
    new_offset = None

    while True:
        text_bot.get_updates(new_offset)

        last_update = text_bot.get_last_update()
        if last_update is None:
            continue

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        text_bot.send_message(last_chat_id, last_chat_text)

        new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()