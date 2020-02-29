from datetime import datetime
from datetime import date
import praw
import getSecrets

reddit = praw.Reddit(client_id=getSecrets.read("redditID.txt"),
                     client_secret=getSecrets.read("redditSecret.txt"),
                     password=getSecrets.read("redditPassword.txt"),
                     user_agent='NLSS Bot by /u/AManNamedLear',
                     username='NorthernlionBot')

sub = "NLSSBotTest"

def post(games, vod):
    print(reddit.user.me())
    subreddit = reddit.subreddit(sub)
    title = constructTitle()
    body = constructBody(games, vod)
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


def constructBody(games, vod):
    header = "# Post NLSS Discussion Thread\n\n"
    docket = "# Docket"
    for game in games:
        docket = docket + "\n" + "* [" + game + "]"
    docket = docket + "\n\n"
    vodText = "# Twitch VOD\n"
    vodText = vodText + "* [Northernlion](" + vod + ")\n\n"
    past = "# Previous Mega Threads\n" + \
        "* [Yeet Yeet](https://www.reddit.com/r/northernlion/search?q=flair%3AMEGA+THREAD&sort=new&restrict_sr=on&t=a)"
    body = header + docket + vodText + past
    return body

