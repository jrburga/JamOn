import socket
import sys
from thread import *
import numpy as np
import json
from jamon.game.game import GameObject
from urllib2 import urlopen


HOST        = '0.0.0.0'
GUEST       = '127.0.0.1'
PORT        = 21385
NUM_CONNS   = 4
NUM_PINGPONGS = 4

MSG_SIZE = 2**20

#TODO: Support "dev mode" and "prod mode":
    # "dev mode" will have everything point to localhost
    # "prod mode" will connect separate devices

#Do we want to be able to allow players to join mid-game?
#> For now, it's designed so that they can only join during 
#> the "form band" phase

class ServerObject(GameObject):
    def __init__(self, num_connections=0):
        super(ServerObject, self).__init__()
        self.port = PORT
        self.ip = HOST
        self.num_connections = num_connections
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_host = False
        # self.bind_to_port()

    def get_ip_address(self):
        return socket.gethostbyname(socket.gethostname())

    def bind_to_port(self):
        """Simple function to bind to the port
        """
        try:
            self.sock.bind((self.ip, self.port))
        except socket.error , msg:
            print 'Bind failed. Error Code: ' + str(msg[0]) + ' Message: ' + msg[1]
            if msg[0] == 48:
                print "The port " + str(self.port) + " is already in use."
                print "Maybe you're already running the program on this machine?"
            #TODO -- Better fail handling
            sys.exit()

    def msg_received(self, msg, sender):
        print 'super message receieved', msg
        try:
            msg = json.loads(msg)
        except Exception, e:
            print e
            return

        # if 'send_to_band' in msg:
        #     del msg['send_to_band']
        assert len(msg) == 1, 'all messages should be wrapped in 1-item dictionary'
        typ = msg.keys()[0]
        print typ
        data = msg[typ]

        if typ == 'game_info':
            if hasattr(self, 'start_game'):
                self.start_game(data)
            else:
                self.stop_searching()
        elif typ == 'action':
            if 'action' in data:
                self.trigger_event(data['event'], action=data['action'])
            else:
                self.trigger_event(data['event'])
        elif typ == 'message':
            print 'message received:', data


class Host(ServerObject):
    def __init__(self, num_connections=NUM_CONNS):
        super(Host, self).__init__(num_connections)
        self.bind_to_port()
        self.is_host = True
        self.sock.listen(self.num_connections)
        self.band_formed = False
        self.band_members = [BandMember(None, self.ip, True, username='Host')]      # Will look like: {"addr[0]+':'+addr[1]":BandMember}

        
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
            print "waiting to accept"
            conn, addr = self.sock.accept()
            print "accepted!"
            if not self.band_formed:
                band_member = BandMember(conn, addr, False)
                self.band_members.append(band_member)
                print 'Connected with ' + addr[0] + ':' + str(addr[1])
                #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
                start_new_thread(self.guest_listen, (band_member,))

        print "Band formed!"
        print "There are " + str(len(self.band_members) + 1) + " band members (including the host)"

    def stop_searching(self):
        print 'stopping search...'
        self.band_formed = True
        # socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((HOST, self.port)) 
        print 'lol'
        # ^dummy socket to kill the accept() statement

    def guest_listen(self, band_member):
        """
        Loop to listen to guests -- should be called in another thread
        """
        # Ping pong for time synchronization
        # self.play_ping_pong(band_member)

        # TODO Send band_member_info to client
        band_member.conn.send(json.dumps({'message':'Send Initial Band Member Info Here'}))

        # This num_blanks_in_a_row is my hacky method for determining if the connection has been broken
        num_blanks_in_a_row = 0
        # Infinite loop so that we constantly listen
        while num_blanks_in_a_row <= 10:
            # Receiving from client
            data = band_member.conn.recv(MSG_SIZE)
            if data:
                self.msg_received(data, band_member)
                num_blanks_in_a_row = 0
            if data == "" or data is None or data.strip() == "":
                num_blanks_in_a_row += 1

        # came out of loop
        band_member.conn.close()
        print "Stopped listening to", band_member

    def send_to_band(self, msg, sender=None):
        """
        Sends a message to the entire band
        """
        # if isinstance(msg, basestring):
        #     for bm, band_member in self.band_members.items():
        #         if bm is not sender:
        #             band_member.conn.send(msg)
        #     return
        msg_json = json.dumps(msg)
        for band_member in self.band_members:
            if band_member.conn:
                band_member.conn.send(msg_json)

        # self.msg_received(msg_json, sender)
        super(Host, self).msg_received(msg_json, sender)

    def msg_received(self, msg, sender):
        """
        data (str): The data in the message
        sender (BandMember): The sender of the message
        """
        # Make sure to check and see if this is the first message 
        # from the new member. If so, fill in their info in the band_member
        # dict

        # try:
        print 'msg receieved', msg
        msg_data = json.loads(msg)
        #First, forward it if it needs to be forwarded
        # if 'send_to_band' in msg_data and msg_data['send_to_band']:
        self.send_to_band(msg_data, sender)

        #Then, call the super method to handle the message
        super(Host, self).msg_received(msg, sender)

        # except Exception as e:
        #     # Data is a string
        #     print e
        #     if msg.strip() == "Band Formed":
        #         self.stop_searching()

class Guest(ServerObject):
    def __init__(self):
        super(Guest, self).__init__()
        self.ip = urlopen('http://ip.42.pl/raw').read()
        # self.bind_to_port()
        self.is_guest = True
        self.host_ip = 'localhost' #Default, but obviously not logical
        self.host_member = None
        self.port = PORT

        self.band_members = [self.host_member]

    def start_game(self, player_list):
        print 'starting game...'
        self.trigger_event('on_scene_change', scene_name='practice', band_members=player_list)

    def set_host_ip(self, host_ip):
        self.host_ip = host_ip

    def connect_to_host(self, timeout=30):
        server_address = (self.host_ip, self.port)
        print 'server address & port:', server_address
        self.sock.settimeout(timeout)
        # err_code = self.sock.connect_ex(server_address)
        self.sock.connect((self.host_ip, PORT))
        self.sock.settimeout(None)
        # if err_code not in [0, None]:
        #     print "WARNING: Connection Error", err_code
        #     return err_code
        # if success, do (1) make host_member, (2) start the listen loop
        self.host_member = BandMember(None, (self.host_ip, self.port), True)

        start_new_thread(self.host_listen, ())
        return True

    def host_listen(self):
        """
        Loop to listen to host -- should be called in another thread
        """
        # TODO Send band_member_info to client

        self.sock.send(json.dumps({'message':'Initial Band Member Info: From Guest'}))
        band_member = BandMember(self.sock, self.ip, False)

        # Infinite loop so that we constantly listen
        while True:
            # Receiving from client
            data = self.sock.recv(MSG_SIZE)
            print "Message Received from", band_member
            self.msg_received(data, band_member)


        # came out of loop
        # band_member.conn.close()
        self.sock.close()
        # print "Stopped listening to", band_emember

    def disconnect_from_host(self):
        print "Disconnecting from host"
        self.sock.close()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_to_band(self, msg, host_only=False):
        """
        Sends to the host with "send_to_band":True
        """
        # if isinstance(msg, basestring):
        #     msg = {"data":msg}
            # In case we wish to send strings for some reason
        
        # send_dict = {"send_to_band":not host_only}
        # send_dict.update(msg)
        msg_str = json.dumps(msg)
        self.sock.send(msg_str)

class BandMember(object):
    """
    Helper class for the Host/Guest to keep track of their band members
    """
    def __init__(self, conn, addr, is_host, username="Guest"):
        """
        conn is a socket object?? TODO
        addr is a tuple of IP address (str) and Port (int)
        """
        super(BandMember, self).__init__()
        self.conn = conn
        self.addr = addr
        self.addr_str = addr[0] + ":" + str(addr[1])
        self.is_host = is_host
        if username != "Guest":
            self.username = username
        else:
            username_id = str(np.random.randint(1000000))
            self.username = username + "_" + username_id

    def info(self):
        return {'ip': self.addr[0], 'username': self.username}

if __name__ == '__main__':
    band_member = BandMember(None, ('1231', '1231'), False)
    print json.dumps([band_member.info()])