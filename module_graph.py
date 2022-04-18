import plotly.express as px
from module_data import get_aggregated_data


aggregated_data = get_aggregated_data()

# NOTE: choropleth uses iso alpha 3 country codes
graph_world_map = px.choropleth(
    aggregated_data,
    locations="iso_alpha",
    hover_name="country",
    hover_data={"country": False, "week": True, "av_sentiment": ":.2f"},
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
    hover_data={"country": False, "av_sentiment": ":.2f"},
)
