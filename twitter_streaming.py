'''Kennedy Ellison
 CMSC 208: Final Project
code based on tutorial from https://www.alexkras.com/how-to-get-user-feed-with-twitter-api-and-python/ '''


import twitter


#user credentials to access Twitter API
access_token = "313326940-H8esCvQa65SVdcPv2vRA79fuciRIFH0mHmlKHils"
access_token_secret = "aRuHOLELittri0XT52fwrn1WEM8GJFY0e7ZEniIR200gF"
consumer_key = "yWBt3OjDy6Q0w3fAGxh9XExYN"
consumer_secret = "kHOsXA7MewuHlzFsu7PmWf6SJPZZI87LS2LdaIWBcE2LChS8xd"




if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API

    twitter_api = twitter.Api(consumer_key,
                  consumer_secret,
                  access_token,
                  access_token_secret,
                  tweet_mode='extended')
    twitter_api.VerifyCredentials()
    tweets=twitter_api.GetUserTimeline(screen_name="drphil", count=200)
    last_tweet=tweets[-1].id

    #loop to get 3200 tweets by modifying call to twitter api with last tweet id
    while len(tweets)<=3200:
        tweets.extend(twitter_api.GetUserTimeline(screen_name="drphil",max_id=last_tweet, count=200))
        last_tweet=tweets[-1].id

    count=0
    file = open("tweets.txt", "w")
    for tweet in tweets:
        print(tweet.full_text)
        file.write(tweets.full_text)
        count+=len(tweet.full_text)
