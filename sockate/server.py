# 786
# code by Tony

import time
import socket
import threading
from .utils import (Reqeust, Response, parse_to_reponse,
                   CloseConnection, parse_to_request)



class Server:
    def __init__(self, host:str, port:int=5000, chunk_size=4096):
        assert chunk_size <= 4096
        self.__host = host
        self.__port = port
        self.__chunk_size = chunk_size
        # creating server main TCP socket
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind((host, port))
        self.__socket.listen(1)
        # useful properties
        self.__keep_running = True
        self.__handlers = {}
        self.__clients = {}


    def run(self):
        while self.__keep_running:
            client, address = self.__socket.accept()
            self.__clients[client] = {
                "send_list" : [],
                "sending" : False
            }
            threading.Thread(
                target=self.__handle_client,
                args=(client, address)
            ).start()


    def __handle_client(self, client:socket.socket, address:str) -> None:
        breaks = 0
        while self.__keep_running and breaks < 30:
            # receiving data size
            size = client.recv(4)

            # break in case socket closes
            if size == b"":
                break

            size = int(size.decode("utf-8"))
            assert size <= self.__chunk_size

            # receiving data
            recv = client.recv(size)

            # handling request
            request = parse_to_request(recv)
            if request.request in self.__handlers.keys():
                response = self.__handlers[request.request](request)
            else:
                response = None

            # retruning answer
            if response != None:
                # close connection
                if isinstance(response, CloseConnection):
                    time.sleep(response.after)
                    client.close()
                    breaks = 30
                    continue

                # make response if it's not Response
                if not isinstance(response, Response):
                    response = Response(
                        request.request,
                        response
                    )
                # set request_id
                response.set_request_id(request.request_id)
                response.parse()
                # send
                self.__send_to_client(client=client, response=response)



    def on_request(self, request:str):
        def wrapper(func):
            if self.__handlers.get(request, False):
                raise RuntimeError(f"Error! There is another request handler for request \"{request}\"")
            self.__handlers[request] = func
            return func

        return wrapper

    def __send_to_client(self, client, response:Response):
        # adding to send list
        self.__clients[client]["send_list"].append(response)
        if self.__clients[client]["sending"] == True:
            return
        # sending process
        self.__clients[client]["sending"] = True
        while len(self.__clients[client]["send_list"]) > 0:
            resp0: Response = self.__clients[client]["send_list"][0]
            client.send(resp0.bytes)
            self.__clients[client]["send_list"].pop(0)
        # function end
        self.__clients[client]["sending"] = False
        return



# server = Server()
#
#
# @server.on_request("ping")
# def ping(r:Reqeust):
#     print(r.message)
#     response = Response(
#         response="ping",
#         message=r.message
#     )
#     return response
#
#
#
# if __name__ == "__main__":
#     server.run()



