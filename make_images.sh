docker run --name mongo-tweet-store -v /Users/dsanford/DSI_Projects/Capstone/Tweet-Data:/data/db -d -p 27017:27017 mongo
docker run --name pyspark-engine -d -p 8888:8888 --link mongo-tweet-store:mongo -v /Users/dsanford/DSI_Projects/Capstone:/home/jovyan/work pyspark-mongo

# to connect
#from os import environ
#print(environ.keys())
#host = environ['MONGO_PORT_27017_TCP_ADDR']
#port = 27017
