#!/Users/dsanford/anaconda/bin/python

import pymongo

mongo_client = pymongo.MongoClient(host='localhost', port=27017)
mongo_db = mongo_client.tweets

print "Existing collections:",mongo_db.collection_names()
print "Number of entries in tweets columns",mongo_db.video_game_tweets.count()
