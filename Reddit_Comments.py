def collect_comment_tree(post, limit):
    path = input("Enter the path to the folder where the file should be saved: ").strip().strip('"')
    #name of the file is "{postID}.jsonl"
    with open(f"{path}/{post}.jsonl", "w", encoding="utf-8", newline="") as f:
        submission = reddit.submission(post)
        #according the PRAW documentation, "limit" based on the number of "MoreComments"
        #If no maximum value is specified, then 'limit=None'. Otherwise, the highest value
        submission.comments.replace_more(limit=limit)

        for comment in submission.comments.list():

            data = {"subreddit_id": comment.subreddit_id, "post_id": comment.link_id, "parent_id": comment.parent_id,
                    "comment_id": comment.id, "created_at": comment.created_utc, "last_modified_at": comment.edited,
                    "score": comment.score}

            f.write(json.dumps(data, ensure_ascii=False, default=str) + "\n")
