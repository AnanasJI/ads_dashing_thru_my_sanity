import plotly.express as px
from dash import dcc
from module_data import get_aggregated_data


aggregated_data = get_aggregated_data()

# NOTE: choropleth uses iso alpha 3 country codes
graph_world_map = px.choropleth(
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

graph_sentiment_timeline = px.line(
    aggregated_data,
    x="week",
    y="av_sentiment",
    title="average sentiment over time",
    color="country",
    hover_name="country",
    hover_data={"country": False, "av_sentiment": ":.2f", "tweet_counts": True},
)

slider_threshold = dcc.Slider(
    0.0,
    1.0,
    0.1,
    value=0.5,
    marks=None,
    tooltip={"placement": "bottom", "always_visible": True},
    id="slider-threshold",
)
