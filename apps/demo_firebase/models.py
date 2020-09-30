from firebase import Firebase

firebaseConfig = {
    'apiKey': "abc",
    'authDomain': "abc",
    'databaseURL': "abc",
    'projectId': "abc",
    'storageBucket': "abc",
    'messagingSenderId': "abc",
    'appId': "abc",
    'measurementId': "abc"
}
firebase = Firebase(firebaseConfig)
db = firebase.database()


class BaseDataTableFireBase:
    table = 'None'

    def __init__(self, table):
        self.table = table

    def create(self, data):
        return db.child(self.table).push(data)

    def get_all(self):
        result = db.child(self.table).get()
        queryset = []
        for item in result.firebases:
            temp = item.val()
            temp['id'] = item.key()
            queryset.append(temp)
        return queryset

    def get(self, id):
        result = db.child(self.table).child(str(id)).get()
        queryset = dict(result.val())
        queryset['id'] = id
        return queryset

    def update(self, id, data):
        return db.child(self.table).child(str(id)).update(data)

    def delete(self, id):
        return db.child(self.table).child(str(id)).remove()
