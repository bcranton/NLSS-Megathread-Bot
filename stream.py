class Stream():
    def __init__(self, channel, live):
        self.channel = channel
        self.live = live
        self.link = f"https://twitch.tv/{self.channel}"

    def setGame(self, game):
        self.game = game
    
    def setLive(self, live):
        self.live = live

    def getGame(self):
        return self.game

    def getLive(self):
        return self.live
    def getName(self):
        return self.channel
    def getLink(self):
        return self.link

class NLSS():
    def __init__(self, docket, guests):
        self.docket = docket
        self.guests = guests
        pass

    def setVOD(self, vod):
        self.vod = vod

    def getVOD(self):
        return self.vod

    def addGuest(self, guest):
        if guest not in self.guests:
            self.guests.append(guest)
    def getGuests(self):
        return self.guests

    def addDocket(self, game):
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
