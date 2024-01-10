import signal
import sys
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCServer

from functions.string_length import string_length
from functions.string_reverse import string_reverse
from functions.manage_files import import_csv
from functions.queries import get_highest_scoring_season_by_player


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


with SimpleXMLRPCServer(('0.0.0.0', 9000), requestHandler=RequestHandler, allow_none=True) as server:
    server.register_introspection_functions()
    server.allow_none = True


    def signal_handler(signum, frame):
        print("received signal")
        server.server_close()

        # perform clean up, etc. here...

        print("exiting, gracefully")
        sys.exit(0)


    # signals
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGHUP, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # register both functions
    server.register_function(string_reverse)
    server.register_function(string_length)
    server.register_function(import_csv)
    server.register_function(get_highest_scoring_season_by_player)

    # start the server
    print("Starting the RPC Server...")
    server.serve_forever()

# readCSV

# convertXml

# storeToDB

# getTop10PlayersWithHighestPtsAvg()

# getHighestScoringSeasonByPlayer(player)

# getTop5PLayersWithMostTripleDoublesSeasons()
