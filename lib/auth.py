from requests.auth import HTTPBasicAuth


class Auth:

    def __init__(self, user, apikey):
        try:
            self.user = user
            self.apikey = apikey
            self.auth = HTTPBasicAuth(self.user, self.apikey)
        except Exception as E:
            print("Error %s" % E)

    def get_auth(self):
        return self.auth
