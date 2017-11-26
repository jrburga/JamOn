import socket
import sys
from thread import *
import numpy as np
import json

LOCAL_HOST  = '127.0.0.1'
PORT        = 21385
NUM_CONNS   = 4


#TODO: Support "dev mode" and "prod mode":
    # "dev mode" will have everything point to localhost
    # "prod mode" will connect separate devices

#Do we want to be able to allow players to join mid-game?
#> For now, it's designed so that they can only join during 
#> the "form band" phase

class ServerObject(object):
    def __init__(self, num_connections):
        self.port = PORT
        self.host = LOCAL_HOST
        self.num_connections = num_connections
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.bind_to_port()

    def get_ip_address(self):
        return socket.gethostbyname(socket.gethostname())

    def bind_to_port(self):
        """Simple function to bind to the port
        """
        try:
            self.sock.bind((self.host, self.port))
        except socket.error , msg:
            print 'Bind failed. Error Code: ' + str(msg[0]) + ' Message: ' + msg[1]
            if msg[0] == 48:
                print "The port " + str(self.port) + " is already in use."
                print "Maybe you're already running the program on this machine?"
            #TODO -- Better fail handling
            sys.exit()

    def msg_received(self, data, sender):
        """
        data (str): The data in the message
        sender (BandMember): The sender of the message
        """
        # Make sure to check and see if this is the first message 
        # from the new member. If so, fill in their info in the band_member
        # dict
        raise NotImplementedError

class Host(ServerObject):
    def __init__(self, num_connections=NUM_CONNS):
        super(Host, self).__init__(num_connections)
        self.is_host = True
        self.sock.listen(self.num_connections)
        self.band_formed = False
        self.band_members = {}      # Will look like: {"addr[0]+':'+addr[1]":BandMember}

    def find_other_players(self):
        """
        Called when the user clicks 'HOST JAM SESH' and would
        like to wait for other players to join the lobby
        Calls _find_other_players_loop in another thread
        """
        print "Looking for other members..."
        start_new_thread(self._find_other_players_loop, ())

        # Band is officially formed now! Make sure to initialize all band_members
    def _find_other_players_loop(self):
        """
        NOTE: Must be killed by calling self.stop_searching()
        """
        while not self.band_formed:
            #wait to accept a connection - blocking call
            conn, addr = self.sock.accept()
            if not self.band_formed:
                band_member = BandMember(conn, addr, False)
                self.band_members[band_member.addr_str] = band_member
                print 'Connected with ' + addr[0] + ':' + str(addr[1])
            
            #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
            start_new_thread(self.guest_listen, (band_member,))

        print "Band formed!"
        print "There are " + str(len(self.band_members.keys()) + 1) + " band members (including the host)"

    def stop_searching(self):
        self.band_formed = True
        socket.socket(socket.AF_INET, 
                      socket.SOCK_STREAM).connect( (self.host, self.port)) 
                      # ^dummy socket to kill the accept() statement

    # Loop to listen to guests
    def guest_listen(self, band_member):
        # TODO Send band_member_info to client
        band_member.conn.send('Welcome to the server. My band member info is: TODO')

        # Infinite loop so that we constantly listen
        while True:
            # Receiving from client
            data = band_member.conn.recv(1024)
            self.msg_received(data, band_member)

        # came out of loop
        band_member.conn.close()
        print "Searching stopped successfully"


    def send_to_guests(self, msg):
        if isinstance(msg, basestring):
            for band_member in self.band_members:
                band_member.conn.send(msg)
            return
        msg_json = json.dumps(msg)
        for band_member in self.band_members:
            band_member.conn.send(msg_json)

    def msg_received(self, msg, sender):
        """
        data (str): The data in the message
        sender (BandMember): The sender of the message
        """
        # Make sure to check and see if this is the first message 
        # from the new member. If so, fill in their info in the band_member
        # dict
        try:
            msg_data = json.loads(msg)
            # TODO: Act on the message
        except Exception as e:
            # Data is a string
            if msg.strip() == "Band Formed":
                self.stop_searching()


class Guest(ServerObject):
    def __init__(self):
        super(Guest, self).__init__()
        self.is_guest = True
        self.host_ip = 'localhost' #Default, but obviously not logical
    
    def set_host_ip(self, host_ip):
        self.host_ip = host_ip
        
    def connect_to_host(self):
        print "trying to connect to host. jk, this isn't implemented yet"
        server_address = (self.host_ip, PORT)
        print 'server address & port:', server_address
        self.sock.connect(server_address)

    def disconnect_from_host(self):
        print "Disconnecting from host"
        self.sock.close()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class BandMember(object):
    """
    Helper class for the Host/Guest to keep track of their band members
    """
    def __init__(self, conn, addr, is_host, username="Guest"):
        """
        conn is a socket object?? TODO
        addr is a tuple of IP address (str) and Port (int)
        """
        self.conn = conn
        self.addr = addr
        self.addr_str = addr[0] + ":" + str(addr[1])
        self.is_host = is_host
        if username != "Guest":
            self.username = username
        else:
            username_id = str(np.random.randint(1000000))
            self.username = username + "_" + username_id



