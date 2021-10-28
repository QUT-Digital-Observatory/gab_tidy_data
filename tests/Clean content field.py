import csv
import re
import pandas as pd

df = pd.read_csv('Sept 6/gab_tidy_data/gabs.csv')

df["text_sans_tags"] = df["content"].str.replace('<.*?>', "")
#print(df["text_sans_tags"])

df["url"] = df["text_sans_tags"].str.extract('(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})')
#print(df["content_2"])

df["text_sans_url"] = df["text_sans_tags"].str.replace('(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})', "")
#print(df["content_3"])

#header = ['Gab ID', 'Text', 'Url', 'Text_sans_URL']
data = [df["id"], df["text_sans_tags"], df["url"], df["text_sans_url"]]

df = pd.DataFrame(data)

df_transposed = df.T

df_transposed.to_csv (r'content_sept7.csv', index = False, header=True)

df_transposed

