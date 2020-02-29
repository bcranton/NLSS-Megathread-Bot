import requests
import json
import time
from pprint import pprint
import postReddit
import getSecrets
#from pprint import pprint

print("Starting NLSS monitorting")

channel = "Trihex"
# channel_id = "14371185"
headers = {'Client-ID': getSecrets.read("twitchID.txt"), }


def main():
    online = False
    gameArray = []
    # Run infinitely, that way its always monitoring for streams
    while True:
        # If the channel is live, we start monitoring for what games they are playing
        if liveCheck():
            print("Appending game to array")
            gameArray.append(getGameName(getGameID()))
            print(f"Appended game to array\n{gameArray}")
            online = True
        elif online:
            # If the channel was online last time we checked but is no longer
            # Wait 2 minutes to make sure it doesn't come back online
            time.sleep(120)
            if not liveCheck():
                # Need to delete "unique" game entries, as sometimes the game being
                # played at the start is left over from last stream
                print(f"Removing unique entries from gameArray\n{gameArray}")
                gameArray = deleteUnique(gameArray)
                # Once those are filtered, lets remove the repeats
                print(f"Removing repeat entries from gameArray\n{gameArray}")
                gameArray = deleteRepeats(gameArray)
                print(f"Getting vod URL")
                vod = getVod()
                print(f"{vod}")
                print(f"Posting to Reddit")
                postReddit.post(gameArray, vod)
                gameArray = []
                online = False
        time.sleep(60)


def liveCheck():
    params = (('user_login', channel),)
    response = requests.get(
        'https://api.twitch.tv/helix/streams', headers=headers, params=params).json()
    # If stream is not live, the string array will be empty
    live = response["data"]
    if live:
        return True
    else:
        print("Not live")
        return False


def getGameID():
    game_id = None
    params = (('user_login', channel),)
    response = requests.get(
        'https://api.twitch.tv/helix/streams', headers=headers, params=params).json()
    game_id = response["data"][0]["game_id"]
    return game_id


def getGameName(game_id):
    name = None
    params = (('id', game_id),)
    response = requests.get(
        'https://api.twitch.tv/helix/games', headers=headers, params=params).json()
    name = response["data"][0]["name"]
    return name


def getVod():
    params = (('login', channel),)
    response = requests.get(
        'https://api.twitch.tv/helix/users', headers=headers, params=params).json()

    user_id = response["data"]["id"]

    params = (('user_id', user_id), ("first", "1"),
              ("period", "day"), ("sort", "views"))
    response = requests.get(
        'https://api.twitch.tv/helix/videos', headers=headers, params=params).json()

    vod = response["data"]["url"]
    return vod


def deleteUnique(gameArray):
    for index in range(len(gameArray) - 1, -1, -1):
        if gameArray.count(gameArray[index]) == 1:
            del gameArray[index]
    return gameArray


def deleteRepeats(gameArray):
    gameArrayEdit = [i for n, i in enumerate(
        gameArray) if i not in gameArray[:n]]
    gameArray = gameArrayEdit
    return gameArray


main()
