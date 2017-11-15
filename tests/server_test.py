
import unittest
import jamon
from server.session import *


class TestServerFunctionality(unittest.TestCase):
    def test_session_connection(self):
        host = Host()
        # client = Client()

# Hacky way of testing with my current setup via scripts:

host = Host()

# testing loop
host.find_other_players()

