# getRatioBot
Find the numerical ratio of likes of a reply to the original tweet

This program uses the Tweepy API to calculate "like ratios" and reply with the result.

To avoid duplicate replies, the program stores that last used tweet in 'last.txt'. The Twitter API only responds to tweets after the last used tweet.
