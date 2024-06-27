# 786
# code by Tony

import time
import socket
import threading
from .utils import Response, Reqeust, parse_to_reponse
from .errors import RecvTimeoutError, SendTimeoutError



class Client:
    def __init__(self, host:str, port:int=5000, chunk_size=4096, timeout:int=30):
        self.__host = host
        self.__port = port
        self.__chunk_size = chunk_size
        self.__timeout = timeout
        self.__csocket:socket.socket = None
        self.__keep_running = True
        self.__requests = {}
        self.__req_id = 0 # request_id

    def connect(self) -> bool:
        self.__csocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__csocket.settimeout(self.__timeout)
        self.__csocket.connect((self.__host, self.__port))
        threading.Thread(target=self.__bg_recv).start()
        return True


    def send(self, request:Reqeust, timeout=30) -> dict:
        self.__req_id += 1
        req_id = self.__req_id
        # add to requests
        self.__requests[req_id] = {
            "done" : False,
            "out" : None
        }
        # send request
        request.set_request_id(req_id)
        request.parse()
        self.__csocket.send(request.bytes)
        # awaiting result
        timer = 0
        while timer < timeout:
            time.sleep(0.05)
            timer += 0.05
            if self.__requests[req_id]["done"] == True:
                response = self.__requests[req_id]
                self.__requests.pop(req_id)
                return response["out"]
        # pop and raise error
        self.__requests.pop(req_id)
        raise SendTimeoutError("No response data!")



    def __bg_recv(self):
        while self.__keep_running:
            # receiving data size
            size = self.__csocket.recv(4)
            # break in case socket closes
            if size == b"":
                break
            size = int(size.decode("utf-8"))
            assert size <= self.__chunk_size
            # receiving data
            recv = self.__csocket.recv(size)

            # returning result
            response = parse_to_reponse(recv)
            check = self.__requests.get(response.request_id, False)
            if check != False:
                self.__requests[response.request_id]["out"] = response
            self.__requests[response.request_id]["done"] = True


    def close(self):
        self.__csocket.close()




# client = Client("127.0.0.1", 5000)
# client.connect()
# r = Reqeust("ping", b"12356")
# print(client.send(r, timeout=3))
# time.sleep(2)
# client.close()


