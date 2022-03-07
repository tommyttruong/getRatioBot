'''
Created on Feb 20, 2022

@author: Tommy Truong
'''

import tweepy
import logging
from keys import keys
from pyasn1.compat.octets import null

# Twitter Developer API keys go here
CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']
# tweepy authorization
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)


# Use a file to store the ID of the most recently used tweet. Only new tweets will replied to.
def get_last_tweet(file):
    f = open(file, 'r')
    lastId = int(f.read().strip())
    f.close()
    return lastId

def put_last_tweet(file, Id):
    f = open(file, 'w')
    f.write(str(Id))
    f.close()
    logger.info("Updated the file with the latest tweet Id")
    return
# Used to display the ratio as a fraction in reduced terms
def reducefract(n, d):
    '''Reduces fractions. n is the numerator and d the denominator.'''
    def gcd(n, d):
        while d != 0:
            t = d
            d = n%d
            n = t
        return n
    assert d!=0, "integer division by zero"
    assert isinstance(d, int), "must be int"
    assert isinstance(n, int), "must be int"
    greatest=gcd(n,d)
    n/=greatest
    d/=greatest
    return n, d
 
def respondToTweet(last_id):
    logger.info("---------------")
    try:
        mentions = api.mentions_timeline(last_id, tweet_mode='extended') # Get a list of all mentions to an account
        if len(mentions) == 0: # End if there are no new mentions
            logger.info("No new mentions....")
            return 
        
        for mention in reversed(mentions): # Iterate through all mentions, reversed to start at the bottom
            logger.info("New mentions detected....")
            # Mentioned tweet. This is the tweet that is @ing the bot
            mentionUser = mention.user # User object of the mention
            mentionScreen = api.get_user(mentionUser.id).screen_name # Use user object to get the screen name.
            # This is the reply, or the tweet "attempting the ratio"
            # Get ID of reply tweet, ID of reply user, reply username, and reply status object
            replyID = mention.in_reply_to_status_id  
            replyUserID = mention.in_reply_to_user_id 
            replyScreen = api.get_user(replyUserID).screen_name
            reply = api.get_status(replyID)
            # Original tweet getting replied to. The tweet getting ratio'd
            # Same as the last chunk of code
            ogID = reply.in_reply_to_status_id
            ogUserId = reply.in_reply_to_user_id
            ogScreen = api.get_user(ogUserId).screen_name
            og = api.get_status(ogID)
    
            if og == null: # Makes sure the reply tweet is an actual reply.
                logger.info("Not a reply....")
                return 
            else:
                logger.info("Reply found....") 
                replyFavorite_count = reply.favorite_count # Number of likes on the reply
                logger.info("Favorite count reply: " + str(replyFavorite_count))
                ogFavorite_count = og.favorite_count # Number of likes on the original tweet
                logger.info("Favorite count OG: " + str(ogFavorite_count))
                
                in_reply_to_status_id = mention.id # Used in api.update_status
                
                # Cases for if its "1 like" or "2 likes" because English is like that. This could be cleaner
                if ogFavorite_count == 0:
                    if replyFavorite_count == 1:
                        status = "@" + mentionScreen + " At the time of this post, " + replyScreen+ "'s reply has " + str(replyFavorite_count) + " like, compared to 0 likes on " + ogScreen + "'s post"
                        api.update_status(status, in_reply_to_status_id)
                    else:
                        status = "@" + mentionScreen + " At the time of this post, " + replyScreen+ "'s reply has " + str(replyFavorite_count) + " likes, compared to 0 likes on " + ogScreen + "'s post"
                        api.update_status(status, in_reply_to_status_id)
                else:
                    ratio = replyFavorite_count / ogFavorite_count
                    n,d = reducefract(replyFavorite_count, ogFavorite_count)
    
                    if replyFavorite_count == 1 & ogFavorite_count == 1:
                        status = "@" + mentionScreen + " At the time of this post, " + replyScreen + "'s reply has " + str(replyFavorite_count) + " like, compared to " + str(ogFavorite_count) + " like on " + ogScreen + "'s post, giving us a ratio of " + str(ratio) + " or " + str(int(n)) + ":" + str(int(d))
                        api.update_status(status, in_reply_to_status_id)
                    elif replyFavorite_count == 1:
                        status = "@" + mentionScreen + " At the time of this post, " + replyScreen + "'s reply has " + str(replyFavorite_count) + " like, compared to " + str(ogFavorite_count) + " likes on " + ogScreen + "'s post, giving us a ratio of " + str(ratio) + " or " + str(int(n)) + ":" + str(int(d))
                        api.update_status(status, in_reply_to_status_id)
                    elif ogFavorite_count == 1:
                        status = "@" + mentionScreen + " At the time of this post, " + replyScreen + "'s reply has " + str(replyFavorite_count) + " likes, compared to " + str(ogFavorite_count) + " like on " + ogScreen + "'s post, giving us a ratio of " + str(ratio) + " or " + str(int(n)) + ":" + str(int(d))
                        api.update_status(status, in_reply_to_status_id)    
                    else:
                        status = "@" + mentionScreen + " At the time of this post, " + replyScreen + "'s reply has " + str(replyFavorite_count) + " likes, compared to " + str(ogFavorite_count) + " likes on " + ogScreen + "'s post, giving us a ratio of " + str(ratio) + " or " + str(int(n)) + ":" + str(int(d))
                        api.update_status(status, in_reply_to_status_id)
    except:
        logger.info("Already replied to {}".format(mention.id)) # In the case a
                
    put_last_tweet("last.txt", replyID)
            
if __name__ == "__main__":
    last_id = get_last_tweet("last.txt")
    logger.info(last_id)
    respondToTweet(last_id)
        
        
    
    