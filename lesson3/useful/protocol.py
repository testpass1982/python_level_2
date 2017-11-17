import json
from .configuration import *

from .errors import MandatoryKeyError

class BaseJim:

    def __init__(self, **kwargs):

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __bytes__(self):
        message_json = json.dumps(self.__dict__)
        message_bytes = message_json.encode(encoding='utf-8')
        return message_bytes

    @classmethod
    def create_from_bytes(cls, message_bytes):
        message_json = message_bytes.decode(encoding='utf-8')
        message_dict = json.loads(message_json)
        return cls(**message_dict)

    def __str__(self):
        return str(self.__dict__)

class JMessage(BaseJim):
    def __init__(self, **kwargs):
        if ACTION not in kwargs:
            raise MandatoryKeyError(ACTION)
        if TIME not in kwargs:
            raise MandatoryKeyError(TIME)
        super().__init__(**kwargs)