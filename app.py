from dash import Dash, dcc, html, Input, Output
from module_graph import *


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


@app.callback(Output("sentiment-timeline", "figure"), Input("hovermode", "value"))
def update_hovermode_sentiment_timeline(mode):
    fig = graph_sentiment_timeline
    fig.update_traces(mode="markers+lines")
    fig.update_xaxes(showspikes=True, spikecolor="grey", spikemode="across")
    fig.update_yaxes(showspikes=True, spikecolor="grey")
    fig.update_layout(hovermode=mode)
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
