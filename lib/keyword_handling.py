import re
import numpy as np
import pandas as pd


def keywords_in_tweet(tweet, keyword_list = []):
    return [word for word in keyword_list \
            if len(re.findall(word.lower(), tweet.lower())) > 0]

def restrict_by_keywords(tweets_df, num_keywords, keyword_list = []):
    tweets_df["keyword_matches"] = \
        tweets_df['text'].apply(lambda tweet: keywords_in_tweet(tweet,
                                                                keyword_list))

    tweets_df = \
        tweets_df[tweets_df["keyword_matches"].apply(len) == num_keywords]
    tweets_df["keyword_matches"] = \
        tweets_df["keyword_matches"].apply(lambda x: x.loc[0] if len(x) > 0 \
                                           else np.nan)
    
    return tweets_df
