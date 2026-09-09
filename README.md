# Thesis
This section describes all the code used in the master's thesis.

# File Descriptions
### Reddit_Posts.py
This code is used to collect posts of a subreddit that are in a selected period. The result is saved into a JSONL file. It is used for the comparing with a little part of the dataset (https://zenodo.org/records/14653265) from the paper "https://doi.org/10.1609/icwsm.v19i1.35946".
The following table shows the subreddit and attached period that are to investigate.
| subreddit id | subreddit name | starttime (oldest post) | endtime (latest post) |
| ------------ | -------------- | ----------------------- | --------------------- |
| 7jkxvy | SilverDegenClub | 1675123201.0 | 1701129601.0 |
| 5vinfe | SeveranceAppleTVPlus | 1645315201.0 | 1697760001.0 |
| 6p57y9 | IdeologyPolls | 1658102401.0 | 1704067201.0 |
| 5qpzgw | WorkReform | 1643068801.0 | 1700870401.0 |
| 35ihl | Histoire | 1660694401.0 | 1703980801.0 |
| 64vwu9 | IamSolo | 1671580801.0 | 1703808001.0 |

### Reddit_Comments.py
This code has the same function as the code "Reddit_Posts.py." It also has the relation to the same dataset and paper. The only difference is it collects comments of multiple comments and not posts, as in "Reddit_Posts.py." The code also needs some configurations.

Why are both codes not combined into one code? Reddit generates each hour new tokens. If the execution is longer than an hour, the execution will be broken. With two separate executions, the probability of this case is decreased. Also, the number of requests contains a limit. This makes it easier to control the limit.

### Reddit_DailyCountsData.py
This code gathers all posts published within a specific timeframe from selected subreddits. The comparison is made using a small subset of the "Daily Counts Data" dataset from the paper "https://doi.org/10.1145/3757644". The file of the dataset "Daily Counts Data" can be downloaded via "https://drive.google.com/file/d/14J-jmKaq3HSn7gkL6duhYUWMu8QOOT-0/view?usp=sharing". A description is shown in "https://github.com/behavioral-data/moderator_discourse_public/tree/master".
