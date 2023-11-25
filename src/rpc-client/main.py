import string
import xmlrpc.client

print("connecting to server...")
server = xmlrpc.client.ServerProxy('http://is-rpc-server:9000')

file = "../../docker/volumes/data/all_seasons.csv"

print(f" > {server.string_reverse(string)}")
print(f" > {server.string_length(string)}")

def menu():
    while True:
        print("----------SYSTEMS INTEGRATION----------")
        print("0 -\tClose the Program")
        print("1 -\tTop 10 pLayers with the highest career points average")
        print("2 -\tHighest scoring season for specific player")
        print("3 -\tTop 5 players with the most triple double seasons")
        print("4 -\tQuery4")
        print("5 -\tQuery5")

        while True:
            try:
                selection = input("\tSelect one option: ")
            except Exception:
                selection = input("\tSelect one option: ")
            if selection in range(6):
                break

        if selection==1:
            result = server.getTop10PlayersWithHighestPtsAvg()
            print(result)
            # function to show data
        elif selection==2:
            player = input("\tEnter the player name: ")
            result = server.getHighestScoringSeasonByPlayer(player)
            print(result)
            # function to show data
        elif selection==3:
            result = server.getTop5PLayersWithMostTripleDoublesSeasons() # +10pts, +10ast, +10rebs
            print(result)
            # function to show data
        elif selection==4:
            result = server.escolherQuery()
            print(result)
            # function to show data
        elif selection==5:
            result = server.escolherQuery()
            print(result)
            # function to show data
        elif selection==0:
            break
