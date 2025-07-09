import threading
from rest_framework_simplejwt.tokens import RefreshToken


class EmailThread(threading.Thread):
    def __init__(self, email_obj):
        super().__init__()
        self.email_obj = email_obj

    def run(self):
        self.email_obj.send()


def get_tokens_for_user_util(user):
    """
    Utility function to generate JWT access token with JTI.
    """
    refresh = RefreshToken.for_user(user)
    refresh.access_token["jti"] = refresh["jti"]
    return str(refresh.access_token)
