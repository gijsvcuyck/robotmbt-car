from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn
from src.parking import ParkingSystem, Input, Output
from src.connection import Connection
import threading

@library
class ParkingLib:
    parkerconn : Connection = None
    parker : threading.Thread = None

    def __init__(self):
        self.builtin = BuiltIn()

    @keyword("Start Parking system at port ${parkingport}")
    def startup_parking_system(self, port: int):
        """
        Start up the parking system.
        @param port: Port number for communication
        """
        assert self.parker == None, "Can only run one parking system at once"
        self.parkerconn = Connection(port=port)
        parker :ParkingSystem = ParkingSystem(port=port)
        self.parker = parker.connect()
        self.parkerconn.connect(timeout=2)


    @keyword("Stop the parking system")
    def teardown_parking_system(self):
        """
        Stop the parking system process
        """

        assert self.parker, "No parking system is currently running"
        self.parkerconn.close()
        self.parker.join(timeout=2)
        assert not self.parker.is_alive(),"teardown of parking system failed"
        self.parker = None
        self.parkerconn = None


    @keyword("Send ${value}")
    def send(self,value:Input):
        self.parkerconn.send(value)


    @keyword("Receive")
    def receive(self) -> Output:
        return self.parkerconn.receivedata()
