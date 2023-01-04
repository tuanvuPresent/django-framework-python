import requests

from Example import settings


class ChatWorkService:
    API_URL_BASE = "https://api.chatwork.com/v2"

    def __init__(self):
        self.headers = {"X-ChatWorkToken": settings.X_CHATWORKTOKEN}

    def get_me(self):
        """
       Return:
           dict: Your account information (json)
       """
        url = "{}/me".format(self.API_URL_BASE)
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_my_status(self):
        """
       Return:
            dict: The number of: unread messages, unfinished tasks etc.
       """
        url = "{}/my/status".format(self.API_URL_BASE)
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_my_tasks(self):
        """
       Return:
            list: list of task if there is any otherwise a json error
        """
        url = "{}/my/tasks?".format(self.API_URL_BASE)
        response = requests.get(url, headers=self.headers)
        if response.status_code != 204:
            return response.json()
        else:
            return "You don't have tasks!"

    def get_contacts(self):
        """
        Return:
             list: list of your contacts
        """
        url = "{}/contacts".format(self.API_URL_BASE)
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_rooms(self):
        """
        Return:
             tuple: list of all rooms
        """
        url = "{}/rooms".format(self.API_URL_BASE)
        response = requests.get(url, headers=self.headers)
        return response.json()

    def send_message(self, room_id: int, message: str, subject: str):
        url = "{}/rooms/{}/messages".format(self.API_URL_BASE, room_id, message)
        data = {
            'body': '[info][title]{}[/title]{}[/info]'.format(subject, message),
            'self_unread': 0
        }
        response = requests.post(url, headers=self.headers, data=data)
        return response

    def send_file(self, room_id: int, file_path: str, file_name: str, message: str, subject: str):
        url = "{}/rooms/{}/files".format(self.API_URL_BASE, room_id)
        files = {
            "file": (file_name, file_path),
            "message": '[info][title]{}[/title]{}[/info]'.format(subject, message),
        }
        response = requests.post(url, headers=self.headers, files=files)
        return response
