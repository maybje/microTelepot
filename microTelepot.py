# -*- coding: utf-8 -*-
import urequests as requests
import time
import _thread

class microGram():
    def __init__(self, bot_id=None):
        self.bot_id = bot_id
        self.requestURL = 'https://api.telegram.org/bot{}/getUpdates'.format(self.bot_id)
        self.sendURL = 'https://api.telegram.org/bot{}/sendMessage'.format(self.bot_id)

        with open("last_update_id.csv", "a+") as f: pass
        with open("last_update_id.csv", "r+") as f:
            try:
                self.last_update_id = int(f.readlines()[0])
            except:
                self.last_update_id = 0

    def sendMessage(self, chatId=None, message=None):
        message = message.replace("\n", "%0A")
        try:
            post = requests.post(self.sendURL + "?chat_id=" + str(chatId) + "&text=" + message)
            post.close()
        except:
            try:
                post.close()
            except:
                pass

    def parseResponse(self, response):
        current_update_id = response["result"][0]["update_id"]
        message = response["result"][0]["message"]
        try:
            text = message["text"]
            content_type = "text"
        except:
            text = None
            content_type = "other"
        chat_id = message["from"]["id"]
        from_sender = message["from"]["first_name"]
        try:
            type_command = message["entities"][0]['type']
        except:
            type_command = content_type
        return chat_id, type_command, text, from_sender, current_update_id


    def listen(self):
        flag = False
        try:
            response = requests.get(self.requestURL + "?offset=" + str(-1), timeout=5)
            response_json = response.json()
            response.close()
            _, _, _, _, current_update_id = self.parseResponse(response_json)

            #chat_id, type_command, text, from_sender, current_update_id
            if current_update_id!=self.last_update_id:
                self.last_update_id = current_update_id
                lui = open("last_update_id.csv","w+")
                lui.write(str(self.last_update_id))
                lui.close()

                flag = True
                return flag, response_json
            else:
                return flag,None
        except:
            try:
                response.close()
            except:
                pass
            return flag, None
