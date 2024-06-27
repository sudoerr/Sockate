# Sockate
Simple TCP socket programming in python without any worry about data handling.
Server side and Client side are made and synced and ready to work.

> This is version (0.0.1) and trying to add more functionality like sending files, multiple Responses in server side and ...

### Examples :
#### Server Side:
```python
from sockate import Server, parse_to_request, Response, Reqeust

# create a server instance
s = Server("0.0.0.0", 5000)

# add requests
s.on_request("ping")
def ping(request:Reqeust):
    message = request.message
    print(message)
    return Response(
        "ping",
        "Got ping"
    )

# run server
s.run()
```

#### Client Side :
```python
from sockate import Client, Reqeust, Response

c = Client("127.0.0.1", 5000, timeout=30)
c.connect()
req = Reqeust(
    "ping",
    "Hello"
)
response = c.send(req)
print(response)
c.close()
```

### Why Sockate ?
You can simply handle any request and send your own data over
TCP connection without any worry about any error or problem!



