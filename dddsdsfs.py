import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Example data
data = {
    "Gender": ["Female", "Male", "Other"],
    "Percentage": [51.5, 46, 2.5],
}
df_gender = pd.DataFrame(data)

# Example pie chart
fig_gender = px.pie(df_gender, names="Gender", values="Percentage", hole=0.4)

# Layout
app.layout = dbc.Container(
    [
        html.Div(
            [
                html.H1("Customer demographics", style={"text-align": "center"}),
                html.P("5,027 Users", style={"text-align": "center", "font-size": "20px"}),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure=fig_gender, style={"height": "300px"}), width=4
                ),
                dbc.Col(
                    dcc.Graph(
                        figure=px.bar(
                            x=["18 - 24", "25 - 34", "35 - 44", "45 - 54", "55 - 64", "65+"],
                            y=[770, 1800, 1200, 680, 370, 160],
                            title="Age",
                        ),
                        style={"height": "300px"},
                    ),
                    width=4,
                ),
                dbc.Col(
                    dcc.Graph(
                        figure=px.bar(
                            x=["Some high school", "High school diploma", "Bachelor's degree", "Graduate degree", "Prefer not to say"],
                            y=[46, 1900, 2200, 870, 32],
                            title="Education Level",
                            orientation="h",
                        ),
                        style={"height": "300px"},
                    ),
                    width=4,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        figure=px.choropleth(
                            locations=["CA", "NY", "TX"],  # Replace with real state codes
                            locationmode="USA-states",
                            scope="usa",
                            color=[500, 400, 300],
                            title="Users by State",
                        ),
                        style={"height": "300px"},
                    ),
                    width=6,
                ),
                dbc.Col(
                    dcc.Graph(
                        figure=px.bar(
                            x=["Under $25K", "$25K - $49K", "$50K - $74K", "$75K - $99K", "$100K - $149K", "Over $150K"],
                            y=[690, 1200, 1100, 760, 790, 460],
                            title="Household Income",
                            orientation="h",
                        ),
                        style={"height": "300px"},
                    ),
                    width=6,
                ),
            ]
        ),
    ],
    fluid=True,
)

# Run the app
if __name__ == "__main__":
    app.run_server(port = '8080')
