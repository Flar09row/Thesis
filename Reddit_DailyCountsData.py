def counting_posts_and_comments(subreddit):
    path = input("Enter the path to the folder where the file should be saved: ").strip().strip('"')
    #name of the file is "{subreddit}.json"
    with open(f"{path}/{subreddit}.json", "w", encoding="utf-8", newline="") as f:

        new_posts = reddit.subreddit(subreddit).new(limit=1000)
        attributes = []
        num_posts = 0
        num_com = 0
        for post in new_posts:

            # 1789257601 = day is 2026.09.13 and time is 00:00:01
            if post.created_utc < 1789257601: #if post is older then period, break the loop
                break
            #1789343999 = day is 2026.09.13 and time is 23:59:59
            elif post.created_utc > 1789343999: #if the post is not in the period, check the next post
                continue

            num_posts += 1

            post.comments.replace_more(limit=1000)
            for comment in post.comments.list():
                num_com += 1

                #collecting all attributes of a comment
                attributes.append(vars(comment))

        data = {"number of posts": num_posts, "number of comments": num_com,
                "attributes": attributes}
        f.write(json.dumps(data, ensure_ascii=False, default=str))
