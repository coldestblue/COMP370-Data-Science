import pandas as pd

df = pd.read_csv("IRAhandle_tweets_1.csv")
df_cleaned = (
    df.head(10000)
    .query("language == 'English'")
    .loc[~df['content'].str.contains(r'\?', na=False)]
)

df_cleaned['trump_mention'] = df_cleaned['content'].str.contains(r'\bTrump\b', regex=True).map({True: 'T', False: 'F'})
trump_mentions = df_cleaned['trump_mention'].value_counts()['T']  
df_cleaned = df_cleaned.drop(['external_author_id', 'author', 'region', 'language', 'harvested_date', 'following', 'followers', 'updates',
       'post_type', 'account_type', 'retweet', 'account_category',
       'new_june_2018', 'alt_external_id', 'article_url',
       'tco1_step1', 'tco2_step1', 'tco3_step1'], axis=1)
new_col_order = ['tweet_id', 'publish_date', 'content', 'trump_mention']
df_cleaned = df_cleaned[new_col_order]
df_cleaned.to_csv("dataset.tsv", sep='\t', index=False)

total_rows = len(df_cleaned)
trump_mention_stats = round((trump_mentions/total_rows) * 100, 3)
print(trump_mention_stats) 

results_df = pd.DataFrame(columns=['result', 'value'])
results_df.loc[1] = [trump_mentions, trump_mention_stats]
results_df.to_csv("results.tsv", sep='\t', index=False)






