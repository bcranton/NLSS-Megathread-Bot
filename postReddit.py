#!/usr/bin/python3
import os
from datetime import datetime
from datetime import date
import praw
import stream
from dotenv import load_dotenv
load_dotenv()
reddit_id = os.environ.get("reddit_id")
reddit_secret = os.environ.get("reddit_secret")
reddit_password = os.environ.get("reddit_password")

reddit = praw.Reddit(client_id=reddit_id,
                     client_secret=reddit_secret,
                     password=reddit_password,
                     user_agent='NLSS Bot by /u/AManNamedLear',
                     username='NorthernlionBot')

sub = "NLSSBotTest"


def post(games, vod, guests):
    print(reddit.user.me())
    subreddit = reddit.subreddit(sub)
    title = constructTitle()
    body = constructBody(games, vod, guests)
    post = subreddit.submit(title, selftext=body)
    post.mod.sticky()
    return True


def constructTitle():
    day = datetime.today().strftime('%A')
    today = date.today().strftime("%B %d, %Y")
    if day == "Sunday":
        event = "NLSS Sunday Subscriber Stream Megathread"

    elif day == "Tuesday":
        event = "NLSS Team Unity Tuesday Megathread"

    else:
        event = "NLSS " + day + " Megathread"
    title = event + " -- " + today
    return title


def constructBody(games, vod, guests):
    header = "# Post NLSS Discussion Thread\n\n"

    # Section of the body that contains the docket
    docket = "## Docket"
    for game in games:
        docket = docket + "\n" + "* [" + game + "]"
    docket = docket + "\n\n"

    guestBody = "## Hosts and Guests\n"
    guestBody = guestBody + f"* [Northernlion](https://twitch.tv/Northernlion)\n"
    if guests:
        for guest in guests:
            guestBody = guestBody + f"[{guest.getName()}]({guest.getLink()})\n"
             

    # Slap in the twitch vod link
    vodText = "\n## Twitch VOD\n"
    vodText = vodText + "* [Northernlion](" + vod + ")\n\n"

    # Link to past threads
    past = "## Previous Mega Threads\n" + \
        "* [Yeet Yeet](https://www.reddit.com/r/northernlion/search?q=flair%3AMEGA+THREAD&sort=new&restrict_sr=on&t=a)"

    # Mash 'em all together
    body = header + guestBody + docket + vodText + past
    return body
