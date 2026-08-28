"""
Sources: https://www.reddit.com/r/redditdev/comments/1149d7b/why_doesnt_apimorechildren_return_the_needed_info/
https://www.reddit.com/r/redditdev/comments/rbr4e1/how_do_you_deal_with_kind_more_links_that_only/
https://gist.github.com/davestevens/4257bbfc82b1e59eeec7085e66314215?utm_source=chatgpt.com
"""

import json
import requests

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

#the comments of the following posts will be collected
posts = ["sta5wl", "v0chmf", "s301pb", "xb7j6v", "t5suyw", "ytw9k0"]

commentIds = set()  #make sure to collect each comment only once.
#list of comments which needs an request to get more information and their replies
moreIds = list()
parentIds = list()

#this function searches for comments that have no detailed information. The id of the comment will be set to the specific list (global variable)
#It exists in two types: 1. The depth of the tree is so long that the comments need their own request
#2. The post or comment contains too many comments/replies to show all in one response.
def searchCommentTree(children):
    for comment in children:
        if comment["data"]["id"] == "_":    #type 1.
            idString = comment["data"]["parent_id"].split("_")
            parentIds.append(idString[1])   #adding the parent_id to the list
            continue
        if comment["data"]["id"] in commentIds: continue
        if comment["kind"] == "more":   #type 2.
            if comment["data"]["children"]:
                #the input for the endpoint '/morechildren/' needs one string with all id of the list
                moreIds.append(",".join(comment["data"]["children"]))  
            continue
        elif comment["kind"] != "t1": continue  #means the part of the response does not contain comments
        else:
            try:
                #a comment contains a minimum of one reply. If it contains multiple replies,
                #the function "searchCommentTree" will be executed again since no replies exists
                #or one of the types without detailed information exists
                if comment["data"]["replies"]["kind"] == "Listing":
                    searchCommentTree(comment["data"]["replies"]["data"]["children"])
            except:
                pass
        commentIds.add(comment["data"]["id"])

#this function also searches for comments, but it starts at the beginning of the comment tree
#each row contains the same function as in "searchCommentTree"
#the difference is the last row. In this case the full comment tree will be written into the file
#the full comment tree also contains all comments with detailed information.
#Therefoer, it is not needed to copy the comments of the function "searchCommentTree" into the file.
def saveComments(childrens, f):
    for comment in childrens:
        if comment["data"]["id"] in commentIds: continue
        if comment["kind"] == "more":
            if comment["data"]["children"]:
                moreIds.append(",".join(comment["data"]["children"]))  
            elif comment["data"]["id"] == "_":
                idString = comment["data"]["parent_id"].split("_")
                parentIds.append(idString[1])
            continue
        elif comment["kind"] != "t1": continue
        else:
            try:
                if comment["data"]["replies"]["kind"] == "Listing":
                    searchCommentTree(comment["data"]["replies"]["data"]["children"])
            except:
                pass
        commentIds.add(comment["data"]["id"])
    f.write(json.dumps(childrens))


#all selected posts will be investigated
for post in posts:

    #response of a comment tree
    response = requests.get(url=f"https://oauth.reddit.com/comments/{post}",
        headers=headers,
        params={
            "limit": 100,
            "depth": 10,
            "sort": "old"
        }
    )

    if response.status_code != 200:
        print(f"Error: {response.status_code} at {post}")
        continue

    data = response.json()
    if data[1]["data"]: #checking if the comment tree contains comments
        pass
    else:
        print(f"{post} has no comments")
        continue

    #opening the file, where the comments will be saved
    with open(f"{path}/Comments_{post}.json", "w", encoding="utf-8") as f:
        f.write("[") #it is important to create a correct JSON format 
        data = data[1].get("data").get("children")  #startpoint of the first comments
        saveComments(data, f)

        #if the comment tree contains comments without details in type 1, all the left comments
        #need another API-request
        if moreIds:
            #each "more" of the comment tree needs its own request
            for newIDs in moreIds:
                response = requests.get(url="https://oauth.reddit.com/api/morechildren",
                    headers=headers,
                    params={
                        "api_type": "json",
                        "link_id": f"t3_{post}",
                        "children": newIDs,
                        "limit_children": False,
                        "sort": "old"
                    }
                )
                if response.status_code != 200:
                    print(f"Error: {response.status_code} at {newIDs} of {post}")
                    continue

                data = response.json()
                #checking if the response contains information
                try:
                    #the structure of this response is different from the first response
                    data = data.get("json").get("data").get("things")
                    if data["data"]:
                        f.write(",")    #makes a list of comments in a correct JSON format
                        saveComments(data, f)
                    else:
                        print(f"Error: no data in {newIDs}")
                        continue
                    #if all left comments are added to the file, a comma is not needed
                    if newIDs != moreIds[len(moreIds) -1]:
                        f.write(",")
                except:
                    print(f"Error: '/morechildren/' has no results")
                    continue

        #if the comment tree contains comments without details in type 2, all the left comments
        #need another API-request
        if parentIds:
            #each comment of type 2 needs its own request
            for newIDs in parentIds:
                response = requests.get(url=f"https://oauth.reddit.com/comments/{post}/_/{newIDs}",
                    headers=headers,
                    params={
                        "limit": 100,
                        "depth": 10,
                        "sort": "old"
                    }
                )
                if response.status_code != 200:
                    print(f"Error: {response.status_code} at {newIDs} of {post}")
                    continue

                data = response.json()
                #checking if the response contains information.
                #the execution is as before in left comments of type 1.
                if data[1]["data"]:
                    pass
                else:
                    print(f"{post} has no comments")
                    continue
                try:
                    data = data[1].get("data").get("children")
                    if data: 
                        f.write(",")
                        saveComments(data, f)
                except:
                    print(f"Error: no data in {newIDs}")
                    continue
                if newIDs != parentIds[len(parentIds) - 1]:
                    f.write(",")

        f.write("]")    #closing the list of comments

    #the ids have no relation to the next post. Therefore, the lists are cleared
    commentIds.clear()
    moreIds.clear()
    parentIds.clear()
