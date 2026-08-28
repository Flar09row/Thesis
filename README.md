# Thesis
This section describes all the code used in the master's thesis.

# File Descriptions
### Reddit_Posts.py
This code is used to send requests to Reddit and collect the responses into multiple files. The requests are executed for multiple subreddits. Therefore, each subreddit gets its own file. The results are used for the comparing with a little part of the dataset (https://zenodo.org/records/14653265) from the paper "https://doi.org/10.1609/icwsm.v19i1.35946". The code needs configurations, for example, tokens, to be valid for an execution. See "#TODO" inside the code.

### Reddit_Comments.py
This code has the same function as the code "Reddit_Posts.py." It also has the relation to the same dataset and paper. The only difference is it collects comments of multiple comments and not posts, as in "Reddit_Posts.py." The code also needs some configurations.

Why are both codes not combined into one code? Reddit generates each hour new tokens. If the execution is longer than an hour, the execution will be broken. With two separate executions, the probability of this case is decreased. Also, the number of requests contains a limit. This makes it easier to control the limit.

### Reddit_DailyCountsData.py
This code gathers all posts published within a specific timeframe from selected subreddits. The comparison is made using a small subset of the "Daily Counts Data" dataset from the paper "https://doi.org/10.1145/3757644". The file of the dataset "Daily Counts Data" can be downloaded via "https://drive.google.com/file/d/14J-jmKaq3HSn7gkL6duhYUWMu8QOOT-0/view?usp=sharing". A description is shown in "https://github.com/behavioral-data/moderator_discourse_public/tree/master".
