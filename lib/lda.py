import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def lda_pipeline(tweets_df, max_df = 0.25, min_df = 2,  num_topics = 2):
    count_vectorizer = CountVectorizer(decode_error="replace",
                                       stop_words="english",
#                                       token_pattern = "\w{6,}",
                                       max_df = 1.0, min_df = 2,
                                       binary = False)
    lda = LatentDirichletAllocation(n_topics=num_topics, random_state = 321,
                                    learning_method="online")

    count_vectorizer.fit(tweets_df["cleaned_text"])
    tweets_count_vectorized = \
        pd.DataFrame(count_vectorizer.transform(tweets_df["cleaned_text"]).todense(),
                     columns = count_vectorizer.get_feature_names())

    tweets_lda = lda.fit_transform(tweets_count_vectorized)

    topic_words = pd.DataFrame(lda.components_.T,
                               index = count_vectorizer.get_feature_names())

    max_meaning = []

    for colname in topic_words.columns:
        sorted_words = \
            topic_words[colname].sort_values(ascending=False).head(10)
        max_meaning.append(zip(sorted_words.index, list(sorted_words)))

    return (tweets_count_vectorized, lda, pd.DataFrame(max_meaning).T)
