def collect_posts_from_period(subreddit, starttime, endtime):
    path = input("Enter the path to the folder where the file should be saved: ").strip().strip('"')
    #name of the file is "{subreddit}.jsonl"
    with open(f"{path}/{subreddit}.jsonl", "w", encoding="utf-8", newline="") as f:
        # "limit" is None because the position of the posts being searched for is unknown.
        new_posts = reddit.subreddit(subreddit).new(limit=None)

        for post in new_posts:

            if post.created_utc < starttime: #if post is older then period, break the loop
                break
            elif post.created_utc > endtime: #if the post is not in the period, check the next post
                continue

            #this attribute is not listed in the documentation, but the known dataset includes it
            try: crosspost_parent_id = post.crosspost_parent
            except: crosspost_parent_id = ""

            data = {"subreddit_id": post.subreddit_id, "crosspost_parent_id": crosspost_parent_id, "post_id": post.id,
                        "created_at": post.created_utc, "updated_at": post.edited, "score": post.score,
                        "upvote_ratio": post.upvote_ratio, "num_comments": post.num_comments}

            f.write(json.dumps(data, ensure_ascii=False, default=str) + "\n")
    print("Done")
