import requests
import requests.auth
import time
import json

# TODO
CLIENT_ID = "<client ID>"
CLIENT_SECRET = "<client secret>"
user_agent = "<platform>:<app ID>:<version string> (by /u/<reddit username>)"

client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)

# TODO
post_data = {"grant_type": "password", "username": "<username>", "password": "<password>"}
headers = {"User-Agent": user_agent}

# TODO: Path of the folder where the files/responses should be saved
path = "<path>"

#requesting the token
token_response = requests.post(
    "https://www.reddit.com/api/v1/access_token",
    auth=client_auth,
    data=post_data,
    headers=headers
)

access_token = token_response.json()["access_token"]

headers = {"Authorization": f"bearer {access_token}",
           "User-Agent": user_agent}


#all subreddits which will be investigated. 
#the unix epoch time was created via "https://www.epochconverter.com/"
#structure: subreddit, timestamp before the post (past in perspective of post), timestamp after the post (present)
subreddits = [["BinanceSupportTickets", 1619827200, 1620000000],
              ["CryptoMoonShoots", 1620864000, 1621036800],
              ["CyberSecurityAdvice", 1619913600, 1620086400],
              ["Anatomy", 1539302400, 1539475200],
              ["MartialArtsCoin", 1539561600, 1539734400],
              ["Pixar", 1540166400, 1540339200],
              ["acturnips", 1540598400, 1540771200]]


for subreddit in subreddits:
    #creating a file for each subreddit. The responses to the requests will be saved in the file
    with open(f"{path}/Reddit_dailyCountsData_{subreddit[0]}.json", "w", encoding="utf-8") as f:
        f.write("[")
        setComma = False
        #parameters for the request. It does not contain the parameter "after", because the start point
        #must be the first post.
        params = {"limit": 100, "show": "all"}

        #this loop sends requests to Reddit with specific parameters. The response to each request contains 100 posts.
        #it will be repeated since the posts are inside a specific timeframe.
        #the request orders the posts in time, from new to old
        while 1:
            time.sleep(1)   #consideration of the request limit
            response = requests.get(f"https://oauth.reddit.com/r/{subreddit[0]}/new",
                                    headers=headers,
                                    params=params)
            if response.status_code != 200:
                print(f"Error: {response.status_code} at {subreddit[0]}")
                break

            data = response.json()
            if not data["data"]["children"]:
                print(f"Error: {subreddit[0]} has no data")
                break
            children = data.get("data").get("children")
            after = data["data"]["after"]   #start point for the next request
            timestamp = children[-1]["data"]["created_utc"] #date the last post was created

            #checking if one of the 100 posts is inside the time frame. If it is so, then copy the response into the file.
            #otherwise, continue the search after the posts.
            if subreddit[2] < timestamp: 
                if not after:
                    print(f"No more posts in {subreddit[0]}") 
                    break
                params["after"] = after
            else:
                if setComma: f.write(",")
                f.write(json.dumps(children))
                if not setComma: setComma = True
                if subreddit[1] > timestamp: break
                else:
                    if not after:
                        print(f"No more posts in {subreddit[0]}") 
                        break
                    params["after"] = after
        f.write("]")

print("Done")
