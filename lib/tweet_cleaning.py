import re
from sklearn.feature_extraction.text import CountVectorizer

def emoji_replacement(tweet, remove = False):
    if remove is False:
        tweet = re.sub(u'[\U0001F601-\U0001F64F]', u' symbol_emoticon ', tweet)
        tweet = re.sub(u'[\U00002702-\U000027B0]', u' symbol_dingbat ', tweet)
        tweet = re.sub(u'[\U0001F680-\U0001F6C5]', u' symbol_map ', tweet)
        tweet = re.sub(u'[\U0001F000-\U0001FFFF]', u' symbol_other ', tweet)
        tweet = re.sub(u'[\U00002000-\U00002FFF]', u' symbol_other ', tweet)
    else:
        tweet = re.sub(u'[\U0001F601-\U0001F64F]', u' ', tweet)
        tweet = re.sub(u'[\U00002702-\U000027B0]', u' ', tweet)
        tweet = re.sub(u'[\U0001F680-\U0001F6C5]', u' ', tweet)
        tweet = re.sub(u'[\U0001F000-\U0001FFFF]', u' ', tweet)
        tweet = re.sub(u'[\U00002000-\U00002FFF]', u' ', tweet)
    
    return tweet

def retweet_check(tweet):
    return len(re.findall(u'^RT @[\w_]+:', tweet)) > 0

def retweet_replacement(tweet, remove = False):
    replacement_string = ' retweet_marker '
    if remove is True:
        replacement_string = ' '
        
    return re.sub(u'^RT @[\w_]+:', replacement_string, tweet)

def hashtags(tweet):
    return " ".join(re.findall(u'#[\w_]+', tweet))

def hashtags_replacement(tweet, remove = False):
    replacement_string = ' hashtag_marker '
    if remove is True:
        replacement_string = ' '
        
    return re.sub(u'#[\w_]+', replacement_string, tweet)

def user_references(tweet):
    return " ".join(re.findall(u'@[\w_]+', tweet))

def user_references_replacement(tweet, remove = False):
    replacement_string = ' user_reference_marker '
    if remove is True:
        replacement_string = ' '

    return re.sub(u'@[\w_]+', replacement_string, tweet)

def link_replacement(tweet, remove = False):
    replacement_string = ' http_link_marker '
    if remove is True:
        replacement_string = ' '

    return re.sub(u'http\S+', replacement_string, tweet)

def garbage_strings_replacement(tweet):
    tweet = re.sub(u'\d+[^\d\s]+', ' ', tweet)
    tweet = re.sub(u'[^\d\s]+\d+', ' ', tweet)
    tweet = re.sub(u'\s_+\S+\s', ' ', tweet)
    tweet = re.sub(u'\s\S+_+\s', ' ', tweet)
    return tweet


def keyword_converter(tweet, keyword_list = [], remove = False):
    for keyword in keyword_list:
        tweet = re.sub(keyword.lower(), ' ', tweet)

    return tweet


def name_conversion(word, name_dict = {}, remove = False):
    if word in name_dict.keys():
        if remove is False:
            return name_dict[word]
        else:
            return ' '
    else:
        return word

def proper_name_converter(tweet, name_dict = {}, remove = False):
    return " ".join([name_conversion(word, name_dict, remove) \
                     for word in tweet.split()])



def clean_tweet(tweet, keyword_list = [], name_dict = {}, remove = False):
    tweet = tweet.lower()
    cleaned = retweet_replacement(tweet, remove)
    cleaned = emoji_replacement(cleaned, remove)
    cleaned = hashtags_replacement(cleaned, remove)
    cleaned = user_references_replacement(cleaned, remove)
    cleaned = link_replacement(cleaned, remove)
    cleaned = garbage_strings_replacement(cleaned)
    cleaned = keyword_converter(cleaned, keyword_list, remove)
    cleaned = proper_name_converter(cleaned, name_dict, remove)

    return cleaned


def clean_tweet_df(tweet_df, keyword_list = [], name_dict = {}, remove = False):
    tweet_df["cleaned_text"] = \
        tweet_df['text'].apply(lambda text:clean_tweet(text, keyword_list,
                                                       name_dict, remove))

    preprocessor = CountVectorizer().build_preprocessor()
    tweet_df["cleaned_text"] = tweet_df["cleaned_text"].apply(preprocessor)

    return tweet_df
