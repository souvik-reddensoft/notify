class Client(object):
    __client = None
    
    def __init__(self, client) -> None:
        self.__client = client
        self.__http_methods = {
            "get": self.__client.get,
            "post": self.__client.post,
            "patch": self.__client.patch,
            "put": self.__client.put,
            "delete": self.__client.delete
        }
    
    def __getitem__(self, method):
        return self.__http_methods[method]