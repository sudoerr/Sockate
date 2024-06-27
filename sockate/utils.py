# 786
# code by Tony

import json
import base64


class Reqeust:
    def __init__(self, request:str, message:bytes, request_id:int=0):
        self.__message = message
        self.__request = request
        self.__request_id = request_id
        self.__data = None
        self.parse()

    def parse(self) -> None:
        self.__data = {
            "request" : self.__request,
            "request_id" : self.__request_id,
            "message" : base64.b64encode(self.__message).decode()
        }
        self.__data = json.dumps(self.__data)
        size = len(self.__data)
        assert size <= 9999
        size = str(size).zfill(4)
        self.__data = size + self.__data


    def set_request_id(self, request_id:int) -> None:
        self.__request_id = request_id

    @property
    def request_id(self) -> int:
        return self.__request_id
    @property
    def request(self) -> str:
        return self.__request
    @property
    def message(self) -> bytes:
        return self.__message
    @property
    def data(self) -> str:
        return self.__data
    @property
    def bytes(self) -> bytes:
        return self.__data.encode("utf-8")

    def __str__(self):
        return f"Request Object : {self.data}"



class Response(Reqeust):
    def __init__(self, response:str, message:bytes, request_id:int=0):
        super().__init__(response, message, request_id)
    @property
    def response(self):
        return self.request

    def __str__(self):
        return f"Response Object : {self.data}"


def parse_to_reponse(data:bytes) -> Response:
    data = data.decode("utf-8")
    data = json.loads(data)
    return Response(
        data["request"],
        base64.b64decode(data["message"]),
        data["request_id"]
    )

def parse_to_request(data:bytes) -> Reqeust:
    data = data.decode("utf-8")
    data = json.loads(data)
    return Reqeust(
        data["request"],
        base64.b64decode(data["message"]),
        data["request_id"]
    )



class CloseConnection:
    def __init__(self, after:float=0):
        self.__after = after

    @property
    def after(self):
        return self.__after
