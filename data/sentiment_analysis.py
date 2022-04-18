import pandas as pd
from transformers import pipeline
import os


directory = os.fsencode("raw")
classifier = pipeline(
    "sentiment-analysis", "distilbert-base-uncased-finetuned-sst-2-english"
)

for file in os.listdir(directory):
    filename = os.fsdecode(file)

    # only process .csv files
    if filename.endswith(".csv"):
        # read csv file into dataframe
        data = pd.read_csv(os.path.join(os.fsdecode(directory), filename)).iloc[:, 1:]
        data["created_at"] = pd.to_datetime(data["created_at"])

        # analyse sentiment of tweets
        tweets = data["text"].values.tolist()
        results = classifier(tweets)

        # append sentiment and confidence score to dataframe
        sentiment_list = [d["label"] for d in results]
        confidence_list = [d["score"] for d in results]
        data["sentiment"] = sentiment_list
        data["confidence"] = confidence_list

        # save new processed data
        # NOTE: will overwrite existing file with the same name if it exists
        data.to_csv("processed_" + filename)
