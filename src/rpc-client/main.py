import time
import xmlrpc.client
from functions.send_csv import send_csv


def connect_to_server(retry_attempts=5, delay_seconds=2):
    for attempt in range(1, retry_attempts + 1):
        try:
            print(f"Connecting to the server (Attempt {attempt}/{retry_attempts})...")
            server = xmlrpc.client.ServerProxy('http://is-rpc-server:9000/RPC2')
            print("Connection successful.")
            return server
        except ConnectionError as ce:
            print(f"Error: Unable to connect to the server. {ce}")
        except Exception as e:
            print(f"Error: An unexpected error occurred. {e}")

        if attempt < retry_attempts:
            print(f"Retrying in {delay_seconds} seconds...")
            time.sleep(delay_seconds)

    raise ConnectionError(f"Failed to connect after {retry_attempts} attempts. Please check the connection.")


def main():
    server = connect_to_server()

    while True:
        print("----------SYSTEMS INTEGRATION----------")
        print("0 -\tClose the Program")
        print("1 -\tTop 10 pLayers with the highest career points average")
        print("2 -\tHighest scoring season for specific player")
        print("3 -\tTop 5 players with the most triple double seasons")
        print("4 -\tQuery4")
        print("5 -\tQuery5")
        print("6 -\tChoose File")

        selection = input("\tSelect one option: ")

        if selection == '1':
            result = server.getTop10PlayersWithHighestPtsAvg()
            print(result)
            # function to show data
        elif selection == '2':
            player = input("\tEnter the player name: ")
            result = server.getHighestScoringSeasonByPlayer(player)
            print(result)
            # function to show data
        elif selection == '3':
            result = server.getTop5PLayersWithMostTripleDoublesSeasons() # +10pts, +10ast, +10rebs
            print(result)
            # function to show data
        elif selection == '4':
            result = server.escolherQuery()
            print(result)
            # function to show data
        elif selection == '5':
            result = server.escolherQuery()
            print(result)
            # function to show data
        elif selection == '6':
            send_csv(server)
        elif selection == '0':
            break


if __name__ == "__main__":
    main()
