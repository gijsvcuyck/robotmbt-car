import socket

DEFAULTHOST = "127.0.0.1"  # Standard loopback interface address (localhost)


"""An abstract connection class, which abstracts away over how you obtain a socket, but contains some utility methods for once you have one."""
class Connection:
    host : str
    port : int
    sock : socket.socket
    
    def __init__(self, port:int,host:str = DEFAULTHOST, socket=None):
        self.host = host
        self.port = port
        self.sock = socket

    """Send some data over the currently opened socket if possible"""
    def send(self,data: str):
        print(f"sending: !{data}")
        if self.sock :
            self.sock.sendall(data.encode())

    """Receive all currently availiable data from the socket"""
    def receivedata(self)-> str:
        retval = bytearray()
        while True:
            data = self.sock.recv(1024)
            retval.extend(data)
            if len(data) < 1024:
                break
        return retval.decode("utf-8").strip("\r\n")
    
    """
        Creates a new socket, and tries to make an connection to an existing socket
        @param: timeout in seconds
    """
    def connect(self,timeout : float =None):
        assert self.sock == None, "cannot make a new connection before closing the old one."
        self.sock = socket.socket()
        if timeout :
            self.soc.settimeout(timeout)
        self.sock.connect((self.host, self.port))

    """Closes the connection"""
    def close(self):
        assert self.sock, "There is no connection to close"
        self.sock.close()
        self.sock = None
