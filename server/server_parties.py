class BandMember(object):
    """
    Helper class for the Host/Guest to keep track of their band members
    """
    count = 0
    def __init__(self, conn, addr, is_host, username=None):
        """
        conn is a socket object?? TODO
        addr is a tuple of IP address (str) and Port (int)
        """
        super(BandMember, self).__init__()
        if username == None:
            self.username = member_names[BandMember.count%len(member_names)]
            BandMember.count += 1
        else:
            self.username = username
        self.conn = conn
        self.addr = addr
        if addr[1]:
            self.addr_str = addr[0] + ":" + str(addr[1])
        else:
            self.addr_str = addr[0]            
        self.is_host = is_host

        self._id = id(self)

    def info(self):
        return {'ip': self.addr[0], 'username': self.username}

    @property
    def ID(self):
        return self._id

if __name__ == '__main__':
    band_member = BandMember(None, ('1231', '1231'), False)
    print json.dumps([band_member.info()])