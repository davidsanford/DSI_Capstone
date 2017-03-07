import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

def lsa_pipeline(tweets_df, max_df = 0.25, min_df = 2, num_components = 100,
                 stop_words = "engilsh"):
    vectorizer = TfidfVectorizer(decode_error="replace", stop_words=stop_words,
                                 max_df = max_df, min_df = min_df,
                                 binary = False)
    
    svd = TruncatedSVD(n_components=num_components, random_state = 321)

    vectorizer.fit(tweets_df["cleaned_text"])

    tweets_vectorized = \
        pd.DataFrame(vectorizer.transform(tweets_df["cleaned_text"]).todense(),
                     columns=vectorizer.get_feature_names())

    tweets_svd = svd.fit_transform(tweets_vectorized)

    return (tweets_svd, vectorizer, svd)

def run_lsa(tweets_df, vectorizer, svd):
    tweets_vectorized = \
        pd.DataFrame(vectorizer.transform(tweets_df["cleaned_text"]).todense(),
                     columns=vectorizer.get_feature_names())

    tweets_svd = svd.transform(tweets_vectorized)

    return tweets_svd
