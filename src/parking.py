from enum import IntEnum, StrEnum, auto
import socket
from typing_extensions import assert_never
import time
import threading
from src.connection import Connection, DEFAULTHOST



DEFAULTPORT = 3000  # Port to listen on (non-privileged ports are > 1023)

class State(IntEnum):
    START = auto()
    SAFE = auto()
    DANGER = auto()
    STOPPED = auto()
    OFF = auto()

class Input(StrEnum):
    SAFE = auto()
    BEEP = auto()
    UNDEFINED = auto()

    """Map strings not matching any of the defined labels to UNDEFINED when using the Input(str) syntax"""
    @classmethod
    def _missing_(cls, _):
        return cls.UNDEFINED
    
class Output(StrEnum):
    PARK = auto()
    STOP = auto()
    OFF = auto()

class ParkingSystem(Connection):
    state : State
    
    def __init__(self,host:str = DEFAULTHOST,port:int =DEFAULTPORT):
        super().__init__(host=host,port=port)
        self.state = State.START

    """ Creates a new thread, which will then start handeling incoming data until the connection is closed
        This version is non-blocking and immediately returns a handle to the created tread"""
    def connect(self) -> threading.Thread :
        thread = threading.Thread(target=self.connect_blocking)
        thread.start()
        return thread

    """ Create a socket connection for this component, and start handeling incoming data until the connection is closed.
        This version is blocking, and onlly returns until the connection is closed."""
    def connect_blocking(self):
        print("now setting up parking server")
        with socket.socket() as s:
            s.bind((self.host, self.port))
            s.listen()
            conn, addr = s.accept()
            self.sock = conn
            print(f"Connected by {addr}")
            thread = threading.Thread(target=self.handleoutputs)
            thread.start()
            while True:
                data = self.receivedata()
                if data == "":
                    print("Connection closed")
                    break
                data = Input(data)
                print(f"received: ?{data}")
                self.handleinput(data)
            self.sock.close()
            self.sock = None


        

    """"Handles an incoming input label"""
    def handleinput(self,label:Input):
        match self.state:
            case State.START:
                if label == Input.SAFE:
                    self.state = State.SAFE
                elif label == Input.BEEP:
                    self.state = State.DANGER
            case State.SAFE | State.DANGER | State.OFF | State.STOPPED:
                pass
            case _:
                assert_never(self.state)

    """ Picks one output to send based on the current state
        This also changes the state as if that output has already happened"""
    def pickoutput(self)-> Output | None:
        match self.state:
            case State.START | State.OFF:
                return None
            case State.SAFE:
                self.state = State.START
                return Output.PARK
            case State.DANGER:
                self.state =State.STOPPED
                return Output.STOP
            case State.STOPPED:
                self.state = State.OFF
                return Output.OFF
            case _:
                assert_never(self.state)

    """Handles sending of outputs based on the current state. 
        This method is meant to be excecuted in a separate thread, and will only return once the socket is closed."""
    def handleoutputs(self):
        while self.sock:
            time.sleep(1)
            output = self.pickoutput()
            if output :
                self.send(output)
            



