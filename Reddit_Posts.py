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

#all subreddits which will be investigated
#the unix epoch time was created via "https://www.epochconverter.com/"
subreddits = {"t5_7jkxvy": {"subname": "SilverDegenClub", "postid": "t3_10prbex", "starttime": 1675123201.0, "endtime": 1701129601.0},
              "t5_5vinfe": {"subname": "SeveranceAppleTVPlus", "postid": "t3_swq9jj", "starttime": 1645315201.0, "endtime": 1697760001.0},
              "t5_6p57y9": {"subname": "IdeologyPolls", "postid": "t3_w2hwna", "starttime": 1658102401.0, "endtime": 1704067201.0},
              "t5_5qpzgw": {"subname": "WorkReform", "postid": "t3_sdf4j1", "starttime": 1643068801.0, "endtime": 1700870401.0},
              "t5_35ihl": {"subname": "Histoire", "postid": "t3_wrpj1x", "starttime": 1660694401.0, "endtime": 1703980801.0},
              "t5_64vwu9": {"subname": "IamSolo", "postid": "t3_zs9zsd", "starttime": 1671580801.0, "endtime": 1703808001.0}}


for subid in subreddits:
    beforeID = subreddits[subid]["postid"]  #start point to investigate the subreddit

    #creating a file for each subreddit. The responses to the requests will be saved in the file
    with open(f"{path}/Subreddit_{subid}.json", "w", encoding="utf-8") as f:
        f.write("[")
        setComma = False

        #this loop sends requests to Reddit with specific parameters. Since a timeframe as a parameter is not possible,
        #the first request starts at the oldest post (as in the known dataset of the paper).
        #the response of each request contains 100 posts. In some cases the known dataset contains more than 100 posts.
        #zherefore, the next request starts at the newest post of the request the round before.
        #it will repeat the same so long since the "endtime" is reached
        while True:
            time.sleep(1)   #consideration of the request limit
            response = requests.get(f"https://oauth.reddit.com/r/{subreddits[subid]['subname']}/search",
                                    headers=headers,
                                    params={
                                        "limit": 100,
                                        "q": "wikipedia",
                                        "sort": "new",
                                        "restrict_sr": True,
                                        "before": beforeID,
                                        "show": "all",
                                        "type": "link"
                                    })
            if response.status_code != 200:
                print(f"Error: {response.status_code} at {subid}")
                break

            data = response.json()
            if not data["data"]["children"]:
                break

            #checking if the "endtime" is reached or all posts of the last request are outside the timeframe
            if data["data"]["children"][0]["data"]["created"] < subreddits[subid]["starttime"]:
                if data["data"]["children"][-1]["data"]["created"] < subreddits[subid]["starttime"]:
                    break
            elif data["data"]["children"][0]["data"]["created"] > subreddits[subid]["endtime"]:
                if data["data"]["children"][-1]["data"]["created"] > subreddits[subid]["endtime"]:
                    break

            if beforeID == subreddits[subid]["postid"]:
                beforeID = data["data"]["before"] 
                if not beforeID: break
            else:
                beforeID = data["data"]["before"] 
                if not beforeID: break
                f.write(",")

            #writing the response into the file
            data = data.get("data").get("children")
            f.write(json.dumps(data))
        f.write("]")
        
print("Done")