from dash import Dash, dcc, html, Input, Output, State, callback_context
from module_components import *
from module_data import get_aggregated_data

# constant values
default_threshold = 0.7
id_slider_threshold = "slider-threshold"
id_graph_world_map = "graph-world_map"
id_graph_sentiment_timeline = "graph-sentiment-timeline"
id_button_threshold = "btn-update-threshold"
id_selector_sentiment_timeline_hovermode = "selector-sentiment-timeline-hovermode"

# get data aggregared by weeks
aggregated_data = get_aggregated_data(threshold=default_threshold)

# components
# NOTE: sliders are dash components, graphs are plotly components
slider_threshold = get_threshold_slider(id_slider_threshold, default_threshold)
graph_world_map = update_world_graph_data(aggregated_data)
graph_sentiment_timeline = update_sentiment_timeline_graph_data(aggregated_data)


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
                        html.Button("Update", id=id_button_threshold, n_clicks=0),
                    ],
                    className="wrapper",
                )
            ],
            className="card",
        ),
        html.Div(
            children=dcc.Graph(id=id_graph_world_map, figure=graph_world_map),
            className="card",
        ),
        html.Div(
            children=[
                dcc.Graph(
                    id=id_graph_sentiment_timeline, figure=graph_sentiment_timeline
                ),
                html.Div(
                    children=[
                        html.H3("Select hovermode:"),
                        dcc.RadioItems(
                            id=id_selector_sentiment_timeline_hovermode,
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
    Output(id_graph_world_map, "figure"),
    Output(id_graph_sentiment_timeline, "figure"),
    Input(id_button_threshold, "n_clicks"),
    State(id_slider_threshold, "value"),
    Input(id_selector_sentiment_timeline_hovermode, "value"),
)
def update(
    update_threshold_btn_n_clicks: int,
    new_threshold: float,
    sentiment_timeline_hovermode: str,
):
    """
    Inputs:
        update_threshold_btn_n_clicks: number of times the update
            button was clicked. It is not used in the function but
            it must be passed in as an input so that the function
            knows when to run. I.e. the function is run everytime the
            update button's n-click property is updated.
        new_threshold: This value is retrieved from the
            slider-threshold's value. This is the new threshold value
            to use for the data (will only use sentiments with a
            confidence value higher than the threshold in the average
            sentiment calculation).
        sentiment_timeline_hovermode: hovermode that the user can
            select to display in the graph.

    Output:
        Updates all graphs in dashboard.
    """
    # get the id of the last button/component that was changed.
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]

    # check if it was the update button that was changed.
    if id_button_threshold in changed_id:
        aggregated_data = get_aggregated_data(threshold=new_threshold)
        new_graph_world_map = update_world_graph_data(aggregated_data)
        new_graph_sentiment_timeline = update_sentiment_timeline_graph_data(
            aggregated_data
        )

    elif id_selector_sentiment_timeline_hovermode in changed_id:
        new_graph_sentiment_timeline = update_sentiment_timeline_hovermode(
            graph_sentiment_timeline, sentiment_timeline_hovermode
        )
        new_graph_world_map = graph_world_map
    else:
        new_graph_world_map = graph_world_map
        new_graph_sentiment_timeline = graph_sentiment_timeline

    return new_graph_world_map, new_graph_sentiment_timeline


if __name__ == "__main__":
    app.run_server(debug=True)
