import datetime
import requests
import os
from dotenv import load_dotenv
load_dotenv()
twitch_id = os.environ.get("twitch_id")
twitch_access_token = os.environ.get("twitch_access_token")
headers = {'Authorization': f"Bearer {twitch_access_token}",
           'Client-ID': twitch_id, }


class Stream():
    def __init__(self, channel, live):
        self.channel = channel
        self.live = live
        self.link = f"https://twitch.tv/{self.channel}"

    def setGame(self):
        gameID = self.getGameID()
        gameName = self.getGameName(gameID)
        self.game = gameName

    def getGame(self):
        return self.game

    def getLive(self):
        return self.live

    def getName(self):
        return self.channel

    def getLink(self):
        return self.link

    def liveCheck(self):
        channel_name = self.getName()
        params = (('user_login', channel_name),)
        response = requests.get(
            'https://api.twitch.tv/helix/streams', headers=headers, params=params).json()
        # If stream is not live, the string array will be empty
        live = response["data"]
        if live:
            print(f"{channel_name} -- LIVE")
            self.live = True
            return True
        else:
            print(f"{channel_name} -- Not live")
            self.live = False
            return False

    def getGameID(self):
        channel_name = self.getName()
        game_id = None
        params = (('user_login', channel_name),)
        response = requests.get(
            'https://api.twitch.tv/helix/streams', headers=headers, params=params).json()
        game_id = response["data"][0]["game_id"]
        return game_id

    def getGameName(self, game_id):
        name = None
        params = (('id', game_id),)
        response = requests.get(
            'https://api.twitch.tv/helix/games', headers=headers, params=params).json()
        name = response["data"][0]["name"]
        return name


class NLSS():
    def __init__(self, docket, guests):
        self.docket = docket
        self.guests = guests
        pass

    def getVOD(self):
        return self.vod

    def addGuest(self, guest):
        if guest not in self.guests:
            self.guests.append(guest)

    def getGuests(self):
        return self.guests

    def addDocket(self, game):
        if (self.docket).count(game) == 2:
            print (f"Not adding {game} to Docket, already in list twice")
            pass
        else:
            print(f"Appended {game} to docket")     
            self.docket.append(game)

    def getDocket(self):
        return self.docket

    def cleanDocket(self):
        self.docket = self.deleteUnique()
        self.docket = self.deleteRepeats()
        return self.docket

    def deleteUnique(self):
        gameArray = self.docket
        for index in range(len(gameArray) - 1, -1, -1):
            if gameArray.count(gameArray[index]) == 1:
                del gameArray[index]
        return gameArray

    def deleteRepeats(self):
        gameArray = self.docket
        # Create an empty list to store unique elements
        uniqueList = []

        # Iterate over the original list and for each element
        # add it to uniqueList, if its not already there.
        for game in gameArray:
            if game not in uniqueList:
                uniqueList.append(game)

        # Return the list of unique elements
        return uniqueList

    def findVOD(self):
        params = (('login', "Northernlion"),)
        response = requests.get(
            'https://api.twitch.tv/helix/users', headers=headers, params=params).json()

        user_id = response["data"][0]["id"]

        params = (('user_id', user_id), ("period", "day"),
                  ("first", "1"), ("sort", "trending"),)
        response = requests.get(
            'https://api.twitch.tv/helix/videos', headers=headers, params=params).json()

        vod = response["data"][0]["url"]
        self.vod = vod
        self.findClip()    

    def findClip(self):
        date = datetime.datetime.utcnow() # <-- get current time in UTC
        date = date + datetime.timedelta(days = -0.5)  # this 12 hours ago
        date = date.replace(second=0, microsecond=0) # remove seconds
        date = date.isoformat("T") + "Z" #convert to RFC3339
    
        clip = {}

        params = (('login', "Northernlion"),)
        response = requests.get('https://api.twitch.tv/helix/users', headers=headers, params=params).json()
        for item in response["data"]:
            user_id = item["id"]

        params = (('broadcaster_id', user_id),("first", "1"),("started_at", date),)
        response = requests.get('https://api.twitch.tv/helix/clips', headers=headers, params=params).json()
        for item in response["data"]:
            title = item['title']
            url = item['url']
            creator_name = item["creator_name"]
            clip = {"title": title, "url": url, "creator_name": creator_name}
        self.clip = clip
    def getClip(self):
        return self.clip
