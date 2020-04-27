#!/usr/bin/python3
import os
import requests
import time
import sys
import stream
import postReddit

from dotenv import load_dotenv
load_dotenv()
twitch_id = os.environ.get("twitch_id")
headers = {'Client-ID': twitch_id, }


def main():
    # Init variables to default values
    Northernlion = stream.Stream("Northernlion", False)
    JSmithOTI = stream.Stream("JSmithOTI", False)
    Alpacapatrol = stream.Stream("Alpacapatrol", False)
    DumbDog = stream.Stream("DumbDog", False)
    Baertaffy = stream.Stream("Baertaffy", False)
    DanGheesling = stream.Stream("DanGheesling", False)
    MichaelAlFox = stream.Stream("MichaelAlFox", False)
    HCJustin = stream.Stream("HCJustin", False)
    guests = [JSmithOTI, Alpacapatrol, DumbDog,
              Baertaffy, DanGheesling, MichaelAlFox, HCJustin]
    NLSS = stream.NLSS([], [])

    # Run infinitely, that way its always monitoring for streams
    print(f"Monitoring {Northernlion.getName()}")
    while True:
        # If the channel is live, we start monitoring for what games they are playing
        if liveCheck(Northernlion.getName()):
            Northernlion.setLive(True)
            print("Finding current game...")
            gameID = getGameID(Northernlion.getName())
            gameName = getGameName(gameID)
            NLSS.addDocket(gameName)
            print(f"Appended {gameName} to docket")
            print(f"Checking guests for docker")

            guestGameID = ""
            guestGameName = ""
            for guest in guests:
                if liveCheck(guest.getName()):
                    guest.setLive(True)
                    guestGameID = getGameID(guest.getName())
                    guestGameName = getGameName(guestGameID)
                    if guestGameName == gameName:
                        print(f"{guest.getName()} added to guests")
                        NLSS.addGuest(guest.getName())

        elif Northernlion.getLive():
            # If the channel was online last time we checked but is no longer
            # Wait 1 minute to make sure it doesn't come back online
            print("Waiting 1 more minute to make sure stream doesn't come back...")
            for remaining in range(60, 0, -1):
                sys.stdout.write("\r")
                sys.stdout.write(f"{remaining} seconds remaining...")
                sys.stdout.flush()
                time.sleep(1)
            print()
            if not liveCheck(Northernlion.getName()):
                # Need to delete "unique" game entries, as sometimes the game being
                # played at the start is left over from last stream
                print(f"Cleaning entries from docket\n{NLSS.getDocket()}")
                NLSS.cleanDocket()
                print(f"Getting vod URL")
                NLSS.setVOD(getVod(Northernlion.getName()))
                print(f"Posting to Reddit")
                postReddit.post(NLSS.getDocket(), NLSS.getVOD(), NLSS.getGuests())

                # Reset variables
                for guest in guests:
                    del guest
                del Northernlion
                del NLSS
                Northernlion = stream.Stream("Northernlion", False)
                JSmithOTI = stream.Stream("JSmithOTI", False)
                Alpacapatrol = stream.Stream("Alpacapatrol", False)
                DumbDog = stream.Stream("DumbDog", False)
                Baertaffy = stream.Stream("Baertaffy", False)
                DanGheesling = stream.Stream("DanGheesling", False)
                MichaelAlFox = stream.Stream("MichaelAlFox", False)
                HCJustin = stream.Stream("HCJustin", False)
                Flackblag = stream.Stream("Flackblag", False)

                guests = [JSmithOTI, Alpacapatrol, DumbDog,
                          Baertaffy, DanGheesling, MichaelAlFox, HCJustin, Flackblag]
                NLSS = stream.NLSS([], [])
        print("Sleeping for 2 minutes before checking again...")
        for remaining in range(120, 0, -1):
            sys.stdout.write("\r")
            sys.stdout.write(f"{remaining} seconds remaining")
            sys.stdout.flush()
            time.sleep(1)
        print()


def liveCheck(channel_name):
    params = (('user_login', channel_name),)
    response = requests.get(
        'https://api.twitch.tv/helix/streams', headers=headers, params=params).json()
    # If stream is not live, the string array will be empty
    live = response["data"]
    if live:
        print(f"{channel_name} -- LIVE")
        return True
    else:
        print(f"{channel_name} -- Not live")
        return False


def getGameID(channel_name):
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


def getVod(channel_name):
    params = (('login', channel_name),)
    import pprint
    response = requests.get(
        'https://api.twitch.tv/helix/users', headers=headers, params=params).json()

    user_id = response["data"][0]["id"]

    params = (('user_id', user_id), ("period", "day"),
              ("first", "1"), ("sort", "trending"),)
    response = requests.get(
        'https://api.twitch.tv/helix/videos', headers=headers, params=params).json()
    pprint.pprint(response)

    vod = response["data"][0]["url"]
    return vod


main()
