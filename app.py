from dash import Dash, dcc, html, Input, Output, State, callback_context
from module_graph import *
from module_update_graphs import *


# create web app
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(
    children=[
        html.Div(
            children=[html.H1(children="Dashboard", className="header-title")],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H3("Select sentiment anaylsis confidence threshold:"),
                        slider_threshold,
                        html.Button("Update", id="btn-update-threshold", n_clicks=0),
                    ],
                    className="wrapper",
                )
            ],
            className="card",
        ),
        html.Div(
            children=dcc.Graph(id="world-map", figure=graph_world_map), className="card"
        ),
        html.Div(
            children=[
                dcc.Graph(id="sentiment-timeline", figure=graph_sentiment_timeline),
                html.Div(
                    children=[
                        html.H3("Select hovermode:"),
                        dcc.RadioItems(
                            id="hovermode",
                            inline=True,
                            options=["x", "x unified", "closest"],
                            value="closest",
                        ),
                    ],
                    className="card-text",
                ),
            ],
            className="card",
        ),
    ],
    className="wrapper",
)


@app.callback(
    Output("world-map", "figure"),
    Output("sentiment-timeline", "figure"),
    State("btn-update-threshold", "id"),
    Input("btn-update-threshold", "n_clicks"),
    State("slider-threshold", "value"),
    Input("hovermode", "value"),
)
def update_threshold_world_map(
    update_threshold_btn_id: str,
    uupdate_threshold_btn_n_clicks: int,
    new_threshold: float,
    sentiment_timeline_hovermode,
):
    """
    Inputs:
        update_threshold_btn_id: id of the update button.
        uupdate_threshold_btn_n_clicks: number of times the update
            button was clicked. It is not used in the function but
            it must be passed in as an input so that the function
            knows when to run. I.e. the function is run everytime the
            update button's n-click property is updated.
        new_threshold: This value is retrieved from the
            slider-threshold's value. This is the new threshold value
            to use for the data (will only use sentiments with a
            confidence value higher than the threshold in the average
            sentiment calculation).

    Output:
        A new world graph.
    """
    # get the id of the last button/component that was changed.
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]

    # check if it was the update button that was changed.
    if update_threshold_btn_id in changed_id:
        # get new aggregated data
        aggregated_data = get_aggregated_data(threshold=new_threshold)

        # NOTE: choropleth uses iso alpha 3 country codes
        new_graph_world_map = px.choropleth(
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

        new_graph_sentiment_timeline = px.line(
            aggregated_data,
            x="week",
            y="av_sentiment",
            title="average sentiment over time",
            color="country",
            hover_name="country",
            hover_data={"country": False, "av_sentiment": ":.2f", "tweet_counts": True},
        )
    elif "hovermode" in changed_id:
        new_graph_sentiment_timeline = update_hovermode_sentiment_timeline(
            graph_sentiment_timeline, sentiment_timeline_hovermode
        )
        new_graph_world_map = graph_world_map
    else:
        new_graph_world_map = graph_world_map
        new_graph_sentiment_timeline = graph_sentiment_timeline

    return new_graph_world_map, new_graph_sentiment_timeline


if __name__ == "__main__":
    app.run_server(debug=True)
