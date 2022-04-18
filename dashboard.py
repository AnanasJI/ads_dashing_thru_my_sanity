import pandas as pd
from enum import Enum
import dash
from dash import dcc, html
import plotly.express as px
import sys


class Label(Enum):
    """
    Enummeration class representing the possible labels from the classifier.
    """

    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    NEUTRAL = "NEUTRAL"


def get_window_sentiment(df: pd.DataFrame, threshold: float = 0.70) -> float:
    """
    Inputs:
        df: dataframe containing window of tweets to get a average sentiment
            across
        threshold: threshold for the confidence score (between 0 and 1) given
            by the classifier of the assigned sentiment. tweets that do not
            meet this threshold will not be conssidered in the calculation.

    Output:
        The average sentiment of the given dataframe. A score of -1 is
            completely negative and a score of 1 is completely positive.
            Type is float.
    """
    pos_counts = 0
    neg_counts = 0
    neu_counts = 0

    for _, row in df.iterrows():
        label, confidence = row["sentiment"], row["confidence"]
        if confidence >= threshold:
            if label == Label.POSITIVE.value:
                pos_counts += 1
            elif label == Label.NEGATIVE.value:
                neg_counts += 1
            elif label == Label.NEUTRAL.value:
                neu_counts += 1
            else:
                sys.exit("Invalid label: " + label)
    return (pos_counts - neg_counts) / max(1, (pos_counts + neg_counts + neu_counts))


def get_windowed_tweets(
    tweets: pd.DataFrame, start_time: pd.Timestamp, end_time: pd.Timestamp
) -> pd.DataFrame:
    """
    Inputs:
        tweets: dataframe of all tweets to query
        start_time: pandas.Timestamp of the start of the time window
            (included).
        end_time: pandas.Timestamp of the end of the time window (excluded).

    Output:
        A dataframe containing only tweets within the inputted time window.
    """
    year_query = f"{start_time.year} <= created_at.dt.year <= {end_time.year}"
    month_query = f"{start_time.month} <= created_at.dt.month <= {end_time.month}"
    day_query = f"{start_time.day} <= created_at.dt.day < {end_time.day}"
    return tweets.query(f"{year_query} and {month_query} and {day_query}")


def aggregate_sentiment_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Input:
        data: dataframe containing all data.

    Output:
        An dataframe of all the data, aggregated by weekly sentiment averages.
    """
    # TODO: change to accept data not just for canada

    # create empty dataframe
    aggregated_data = pd.DataFrame(
        columns=["week", "country", "av_sentiment", "iso_alpha"]
    )

    # format pd.Timestamp into a string
    time_string_format = "%Y-%m-%d"

    # set start week to aggregate from
    week = pd.Timestamp("2019-01-01")

    index = 0
    while week <= pd.Timestamp.today():
        next_week = week + pd.DateOffset(days=7)
        window_df = get_windowed_tweets(data, week, next_week)
        score = get_window_sentiment(window_df)
        aggregated_data.loc[index] = [
            week.strftime(time_string_format),
            "Canada",
            score,
            "CAN",
        ]
        index += 1
        week = next_week

    return aggregated_data.set_index("week")


if __name__ == "__main__":
    data = pd.read_csv("data/CAN_data.csv").iloc[:, 1:]
    data["created_at"] = pd.to_datetime(data["created_at"])

    aggregated_data = aggregate_sentiment_data(data)

    # create graph
    fig = px.choropleth(
        aggregated_data,
        locations="iso_alpha",
        color="av_sentiment",
        hover_name="country",
        animation_frame=aggregated_data.index,
        color_continuous_scale="Plasma",
        range_color=(-1, 1),
        height=600,
    )

    # create web app
    app = dash.Dash()
    app.layout = html.Div([dcc.Graph(id="sentiment_over_time", figure=fig)])

    app.run_server(debug=True)
