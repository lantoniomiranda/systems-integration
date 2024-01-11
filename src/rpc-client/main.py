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
        print("1 -\tHighest scoring season for specific player")
        print("2 -\tPLayers with triple double seasons")
        print("3 -\tTop 5 Colleges")
        print("4 -\tChoose File")

        selection = input("\tSelect one option: ")

        if selection == '1':
            player = input("\tEnter the player name: ")
            result = server.get_highest_scoring_season_by_player(player)
            print(result)
        elif selection == '2':
            result = server.get_players_with_tripleDoubleSeasons() # +10pts, +10ast, +10rebs
            print(result)
        elif selection == '3':
            result = server.get_top5_colleges()
            print(result)
        elif selection == '4':
            send_csv(server)
        elif selection == '0':
            break


if __name__ == "__main__":
    main()
