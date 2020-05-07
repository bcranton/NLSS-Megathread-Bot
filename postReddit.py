#!/usr/bin/python3
import os
from datetime import datetime
from datetime import date
import time
import praw
import stream
from dotenv import load_dotenv
load_dotenv()
reddit_id = os.environ.get("reddit_id")
reddit_secret = os.environ.get("reddit_secret")
reddit_password = os.environ.get("reddit_password")


sub = "NLSSBotTest"


class Construct():
    def __init__(self, games, vod, guests, clip):
        self.games = games
        self.vod = vod
        self.guests = guests
        self.clip = clip
        self.constructTitle()
        self.constructBody()

    def getGames(self):
        return self.games

    def getVOD(self):
        return self.vod

    def getGuests(self):
        return self.guests

    def constructTitle(self):
        day = datetime.today().strftime('%A')
        today = date.today().strftime("%B %d, %Y")
        if day == "Sunday":
            event = "NLSS Sunday Subscriber Stream Megathread"

        elif day == "Tuesday":
            event = "NLSS Team Unity Tuesday Megathread"

        else:
            event = "NLSS " + day + " Megathread"
        title = event + " -- " + today
        self.title = title

    def getTitle(self):
        return self.title

    def constructBody(self):
        header = "# Post NLSS Discussion Thread\n\n---------------------------------------------\n\n"

        # Section of the body that contains the docket
        docket = "### Docket\n"
        games = self.getGames()
        for game in games:
            docket = docket + f"* {game}\n"
        docket = docket + "\n\n"

        guestBody = "### Hosts and Guests\n"
        guestBody = guestBody + \
            f"* [Northernlion](https://twitch.tv/Northernlion)\n"
        guests = self.getGuests()
        if guests:
            for guest in guests:
                guestBody = guestBody + \
                    f"\n* [{guest.getName()}]({guest.getLink()})\n"

        # Today's top clip
        clip = ""
        try:
            creator = (self.clip).get("creator_name")
            url = (self.clip).get("url")
            title = (self.clip).get("title")

            clip = f"\n*Today's Most Pogged Moment, brought to you by [{creator}](https://twitch.tv/{creator})*\n"
            clip = clip + f"\n**[{title}]({url})**\n"
        except:
            pass

        # Slap in the twitch vod link
        vodText = f"\n----------------------------------------------\n\n### [Twitch VOD]({self.getVOD()})\n\n"
        # Link to past threads
        past = "### [Previous Mega Threads](https://www.reddit.com/r/northernlion/search?q=flair%3AMEGA+THREAD&sort=new&restrict_sr=on&t=a)"

        footer = "\n\n----------------------------------------------\n\n^(Bot created by ) ^[/u/AManNamedLear](https://www.reddit.com//u/AManNamedLear) ^(| Find me on) ^[GitHub](https://github.com/bcranton/NLSS-Megathread-Bot)"
        # Mash 'em all together
        body = header + docket + guestBody + clip + vodText + past + footer
        self.body = body

    def getBody(self):
        return self.body


def post(games, vod, guests, clip):
    # Make sure we can establish a connection to reddit
    connected = False
    while not connected:
        try:
            reddit = praw.Reddit(client_id=reddit_id,
                                client_secret=reddit_secret,
                                password=reddit_password,
                                user_agent='NLSS Bot by /u/AManNamedLear',
                                username='NorthernlionBot')
            connected = True
        except:
            time.sleep(30)
            pass

    print(reddit.user.me())
    subreddit = reddit.subreddit(sub)

    content = Construct(games, vod, guests, clip)

    post = subreddit.submit(content.getTitle(), selftext=content.getBody())
    post.mod.sticky()
    post.mod.flair(text="[MEGA THREAD]")
    return True
