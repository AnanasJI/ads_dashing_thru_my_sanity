import pandas as pd
import plotly.express as px


def update_world_graph_data(aggregated_data: pd.DataFrame):
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
        animation_frame="week",
        color="av_sentiment",
        color_continuous_scale=px.colors.diverging.RdBu,
        color_continuous_midpoint=0,
        range_color=(-1, 1),
        height=600,
    )


def update_sentiment_timeline_graph_data(aggregated_data: pd.DataFrame):
    return px.line(
        aggregated_data,
        x="week",
        y="av_sentiment",
        title="average sentiment over time",
        color="country",
        hover_name="country",
        hover_data={"country": False, "av_sentiment": ":.2f", "tweet_counts": True},
    )


def update_sentiment_timeline_hovermode(fig, mode):
    fig.update_traces(mode="markers+lines")
    fig.update_xaxes(showspikes=True, spikecolor="grey", spikemode="across")
    fig.update_yaxes(showspikes=True, spikecolor="grey")
    fig.update_layout(hovermode=mode)
    return fig
