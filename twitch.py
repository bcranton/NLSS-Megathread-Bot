#!/usr/bin/python3
import os
import requests
import time
import sys
import stream
import postReddit

# List of possible cohosts
cohosts = ["JSmithOTI",
           "Alpacapatrol",
           "DumbDog",
           "Baertaffy",
           "DanGheesling",
           "MichaelAlFox",
           "HCJustin",
           "Flackblag",
           "Sinvicta",
           "CobaltStreak"]


def main():
    # Init variables to default values
    guests = cleanup(cohosts)
    Northernlion = stream.Stream("Northernlion", False)
    NLSS = stream.NLSS([], [])
    online = False

    # Run infinitely, that way its always monitoring for streams
    print(f"Monitoring {Northernlion.getName()}")
    while True:
        # If the channel is live, we start monitoring for what games they are playing
        if Northernlion.liveCheck():
            online = True
            print("Finding current game...")
            Northernlion.setGame()
            game = Northernlion.getGame()
            NLSS.addDocket(game)
            print(f"Checking for guests...")
            for guest in guests:
                if guest not in NLSS.getGuests():
                    guest.liveCheck()
                    if guest.getLive():
                        guest.setGame()
                        guestGame = guest.getGame()
                        if guestGame == game:
                            print(f"{guest.getName()} added to guests")
                            NLSS.addGuest(guest)
                else:
                    print(f"{guest.getName()} not added, already in list")

        elif online:
            # If the channel was online last time we checked but is no longer
            # Wait 2 minutes to make sure it doesn't come back online
            print("Waiting 3 more minutes to make sure stream doesn't come back...")
            for remaining in range(180, 0, -1):
                sys.stdout.write("\r")
                sys.stdout.write(f"{remaining} seconds remaining...")
                sys.stdout.flush()
                time.sleep(1)
            print()
            if not Northernlion.liveCheck():
                # Need to delete "unique" game entries, as sometimes the game being
                # played at the start is left over from last stream
                print(f"Cleaning entries from docket\n{NLSS.getDocket()}")
                NLSS.cleanDocket()
                print(f"Getting vod URL")
                NLSS.findVOD()
                print(f"Posting to Reddit")
                postReddit.post(NLSS.getDocket(),
                                NLSS.getVOD(), NLSS.getGuests(), NLSS.getClip())

                # Reset variables
                online = False
                for guest in guests:
                    del guest
                del Northernlion
                del NLSS
                guests = cleanup(cohosts)
                Northernlion = stream.Stream("Northernlion", False)
                NLSS = stream.NLSS([], [])

        print("Sleeping for 1 minute before checking again...")
        for remaining in range(60, 0, -1):
            sys.stdout.write("\r")
            sys.stdout.write(f"{remaining} seconds remaining")
            sys.stdout.flush()
            time.sleep(1)
        print()


def cleanup(cohosts):
    guests = []
    for channel in cohosts:
        guests.append(stream.Stream(channel, False))
    return guests


main()
