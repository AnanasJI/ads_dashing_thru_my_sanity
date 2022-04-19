import pandas as pd
from dash import dcc
import plotly.express as px


def update_world_graph_data(aggregated_data: pd.DataFrame):
    """
    Inputs:
        aggregated_data: data to plot.

    Output:
        updated world map graph.
    """
    return px.choropleth(
        aggregated_data,
        locations="iso_alpha",
        hover_name="country",
        hover_data={
            "country": False,
            "week": True,
            "iso_alpha": False,
            "av_sentiment": ":.2f",
            "tweet_counts": True,
        },
        title="World Map of Average Sentiment",
        animation_frame="week",
        color="av_sentiment",
        color_continuous_scale=px.colors.diverging.RdBu,
        color_continuous_midpoint=0,
        range_color=(-1, 1),
        height=600,
    )


def update_sentiment_timeline_graph_data(aggregated_data: pd.DataFrame):
    """
    Inputs:
        aggregated_data: data to plot.

    Output:
        updated sentiment timeline graph.
    """
    return px.line(
        aggregated_data,
        x="week",
        y="av_sentiment",
        title="Average Sentiment Timeline",
        color="country",
        hover_name="country",
        hover_data={"country": False, "av_sentiment": ":.2f", "tweet_counts": True},
    )


def update_sentiment_timeline_hovermode(fig, mode: str):
    """
    Inputs:
        fig: the sentiment timeline graph/figure. Unsure of data structure
            for typehinting.
        mode: hovermode to change to.

    Output:
        updated sentiment timeline graph using new hovermode.
    """
    fig.update_traces(mode="markers+lines")
    fig.update_xaxes(showspikes=True, spikecolor="grey", spikemode="across")
    fig.update_yaxes(showspikes=True, spikecolor="grey")
    fig.update_layout(hovermode=mode)
    return fig


def get_threshold_slider(id: str, value: float):
    """
    Inputs:
        id: id for component.
        value: value for the slider to be set to.

    Output:
        dash slider component to allow the user to set the confidence
            threshold. Tweets with a sentiment analysis confidence value less
            than this value will be disregarded in the average calculation.
    """
    return dcc.Slider(
        0.0,
        1.0,
        0.1,
        value=value,
        marks=None,
        tooltip={"placement": "bottom", "always_visible": True},
        id=id,
    )
