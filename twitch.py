#!/usr/bin/python3
import os
import requests
import time
import sys
import postReddit

from dotenv import load_dotenv
load_dotenv()
twitch_id = os.environ.get("twitch_id")


channel_name = "Northernlion"

headers = {'Client-ID': twitch_id, }


def main():
    print (f"Monitoring {channel_name}")
    # Init variables to default values
    online = False
    gameArray = []

    # Run infinitely, that way its always monitoring for streams
    while True:
        # If the channel is live, we start monitoring for what games they are playing
        if liveCheck():
            print("Finding current game...")
            gameID = getGameID()
            gameName = getGameName(gameID)
            gameArray.append(gameName)
            print(f"Appended {gameName} to array")
            online = True
        elif online:
            # If the channel was online last time we checked but is no longer
            # Wait 2 minutes to make sure it doesn't come back online
            print("Waiting 1 more minute to make sure stream doesn't come back...")
            for remaining in range(60, 0, -1):
                sys.stdout.write("\r")
                sys.stdout.write(f"{remaining} seconds remaining...")
                sys.stdout.flush()
                time.sleep(1)
            print()
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

                # Reset variables
                gameArray = []
                online = False
        print("Sleeping for 2 minutes before checking again...")
        for remaining in range(120, 0, -1):
            sys.stdout.write("\r")
            sys.stdout.write(f"{remaining} seconds remaining")
            sys.stdout.flush()
            time.sleep(1)
        print()


def liveCheck():
    params = (('user_login', channel_name),)
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
    params = (('user_login', channel_name),)
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
    params = (('login', channel_name),)
    import pprint
    response = requests.get(
        'https://api.twitch.tv/helix/users', headers=headers, params=params).json()

    user_id = response["data"][0]["id"]

    params = (('user_id', user_id), ("period", "day"), ("first", "1"), ("sort", "trending"),)
    response = requests.get(
        'https://api.twitch.tv/helix/videos', headers=headers, params=params).json()
    pprint.pprint(response)

    vod = response["data"][0]["url"]
    return vod


def deleteUnique(gameArray):
    for index in range(len(gameArray) - 1, -1, -1):
        if gameArray.count(gameArray[index]) == 1:
            del gameArray[index]
    return gameArray


def deleteRepeats(gameArray):

    # Create an empty list to store unique elements
    uniqueList = []

    # Iterate over the original list and for each element
    # add it to uniqueList, if its not already there.
    for game in gameArray:
        if game not in uniqueList:
            uniqueList.append(game)

    # Return the list of unique elements
    return uniqueList
main()
