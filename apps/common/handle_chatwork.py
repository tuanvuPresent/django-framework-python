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
        url = f"{self.API_URL_BASE}/me"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_my_status(self):
        """
       Return:
            dict: The number of: unread messages, unfinished tasks etc.
       """
        url = f"{self.API_URL_BASE}/my/status"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_my_tasks(self):
        """
       Return:
            list: list of task if there is any otherwise a json error
        """
        url = f"{self.API_URL_BASE}/my/tasks?"
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
        url = f"{self.API_URL_BASE}/contacts"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_rooms(self):
        """
        Return:
             tuple: list of all rooms
        """
        url = f"{self.API_URL_BASE}/rooms"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def send_message(self, room_id: int, message: str, subject: str):
        url = f"{self.API_URL_BASE}/rooms/{room_id}/messages"
        data = {
            'body': f'[info][title]{subject}[/title]{message}[/info]',
            'self_unread': 0,
        }
        return requests.post(url, headers=self.headers, data=data)

    def send_file(self, room_id: int, file_path: str, file_name: str, message: str, subject: str):
        url = f"{self.API_URL_BASE}/rooms/{room_id}/files"
        files = {
            "file": (file_name, file_path),
            "message": f'[info][title]{subject}[/title]{message}[/info]',
        }
        return requests.post(url, headers=self.headers, files=files)
