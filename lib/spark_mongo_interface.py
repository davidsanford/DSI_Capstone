import pandas as pd
from os import environ
from pyspark.sql import SparkSession

def load_tweets_from_mongo(ip = environ['MONGO_PORT_27017_TCP_ADDR'], collection = "unfiltered_tweets"):
    location = "mongodb://"+ip+":27017/"+collection+".tweets"

    spark_session = (SparkSession
                     .builder
                     .appName("testApp")
                     .config('spark.mongodb.input.uri',location)
                     .config('spark.mongodb.output.uri',location)
                     .getOrCreate())

    tweets_spark = \
        spark_session.read.format("com.mongodb.spark.sql.DefaultSource").load()
    tweets_spark = tweets_spark[['text','lang']]
    tweets_spark = tweets_spark.filter(tweets_spark["lang"]=="en")
    tweets_spark = tweets_spark[['text']].dropna()
    
    tweets_pandas = pd.DataFrame(tweets_spark.collect())
    tweets_pandas.columns = tweets_spark.columns

    #tweets_pandas.dropna(inplace=True)

    #tweets_pandas = \
    #    tweets_pandas[tweets_pandas["lang"] == "en"][["text"]].dropna()

    spark_session.stop()
    
    return tweets_pandas
