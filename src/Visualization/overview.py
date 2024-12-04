from dash import callback, dcc, html, Output, Input, dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from plotly import graph_objects as go
import random
from datetime import datetime
import numpy as np
import dash_visualize as dv

# dataset
data = pd.read_csv("./Data/Club/all_data_of_clubs.csv")
data.rename(columns={"Unnamed: 0": "Team"}, inplace=True)
midfielder_data = pd.read_csv("./Data/Stats_csv/Processed_Midfielder_data.csv")
forward_data = pd.read_csv("./Data/Stats_csv/Processed_Forward_data.csv")
defender_data = pd.read_csv("./Data/Stats_csv/Processed_Defender_data.csv")
goalkeeper_data = pd.read_csv("./Data/Stats_csv/Processed_Goalkeeper_data.csv")

attacking_features = ['Goals', 'Goals per match', 'Penalties scored', 'Shots', 'Shots on target', 'Big Chances Created', 'Shooting accuracy %']
attacking_data = data[['Team'] + attacking_features]
defensive_features = ['Clean sheets', 'Goals Conceded', 'Tackles', 'Tackle success %', 'Errors leading to goal', 'Interceptions']
defensive_data = data[['Team'] + defensive_features]
control_features = ['Passes', 'Passes per match', 'Pass accuracy %', 'Crosses', 'Cross accuracy %']
control_data = data[['Team'] + control_features]

control_fig = px.bar(
    control_data.melt(id_vars='Team', value_vars=control_features, var_name='Metric', value_name='Value'),
    x='Team', y='Value', color='Metric',
    barmode='group',
    title="Comparison of Control Metrics Across Teams"
)

attack_data_corr = data[['Goals', 'Goals per match', 'Penalties scored', 'Shots', 'Shots on target',
                         'Big Chances Created', 'Shooting accuracy %', 'Passes', 'Passes per match',
                         'Pass accuracy %']].corr()

heatmap_data = attack_data_corr.reset_index().melt(id_vars='index')
heatmap_data.columns = ['Feature1', 'Feature2', 'Correlation']

defense_data_corr = data[['Clean sheets', 'Goals Conceded', 'Tackles', 'Tackle success %', 'Interceptions', 'Saves',
                          'Blocked shots', 'Clearances', 'Headed Clearance', 'Aerial Battles/Duels Won', 'Own goals',
                          'Passes', 'Passes per match', 'Pass accuracy %']].corr()


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title="Visualization App")

# layout
app.layout = dbc.Container([
    html.Div([
        html.H2("Premier League", style={"text-align": "center"}),
        html.H3("2024/25", style={"text-align": "center", "font-size": "20px"}),
        html.Hr(),
        dbc.Row(dbc.Col(html.P(style={'font-size': '16px', 'margin': 'auto', 'width': '90%', 'opacity': '70%'}, 
            children='''To understand the future, we often look to the past. This dashboard provides a detailed breakdown of Teams and Players—two critical criteria for evaluating the strength of the top clubs.'''))),
        html.Hr(),
        dbc.Row(dbc.Col(html.H4(children='Overview'))),
        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(id="age-bar", config={"displayModeBar": False}, style={"height": "330px"}), 
                type="circle", color="#f79500"), width=6),
            dbc.Col(dcc.Loading(dcc.Graph(id="age-violin", config={"displayModeBar": False}, style={"height": "330px"}), 
                type="circle", color="#f79500"), width=6),
        ]),
        html.Br(),
        dbc.Row([dbc.Col(dcc.Loading(dcc.Graph(id="over-under-25", config={"displayModeBar": False}, 
            style={"height": "600px", "width": "100%", "margin": "auto", "display": "block"}), type="circle", color="#f79500"), 
            width={"size": 6, "offset": 3}, style={"textAlign": "center"})]),
        html.Br(),
        dbc.Row(dbc.Col(html.P(style={'font-size': '16px', 'margin': 'auto', 'width': '90%', 'opacity': '70%'}, 
            children='The chart above breaks down the Age Distribution, providing perspective based on Position or general analysis or 25-year-old division.'))),
        html.Hr(),
        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(figure=px.line(attacking_data.melt(id_vars='Team', value_vars=attacking_features, 
                var_name='Metric', value_name='Value'), x='Team', y='Value', color='Metric', 
                title="Attacking Metrics Trends Across Teams")), type="circle", color="#f79500"), width=4),
            dbc.Col(dcc.Loading(dcc.Graph(figure=px.bar(defensive_data.melt(id_vars='Team', value_vars=defensive_features, 
                var_name='Metric', value_name='Value'), x='Team', y='Value', color='Metric', 
                title="Defensive Metrics Distribution Across Teams", barmode='stack')), type="circle", color="#f79500"), width=4),
            dbc.Col(dcc.Loading(dcc.Graph(figure=px.bar(control_data.melt(id_vars='Team', value_vars=control_features, 
                var_name='Metric', value_name='Value'), x='Team', y='Value', color='Metric', 
                barmode='group', title="Comparison of Control Metrics Across Teams")), 
                type="circle", color="#f79500"), width=4),
        ]),
        html.Br(),
        html.Hr(),
        dbc.Row([
            dbc.Col(dcc.Loading(dcc.Graph(figure=px.imshow(attack_data_corr, x=attack_data_corr.columns, 
                y=attack_data_corr.columns, zmin=-1, zmax=1, color_continuous_scale='RdBu', 
                title="Correlation Heatmap of Attack Metrics", labels={'color': 'Correlation'})), 
                type="circle", color="#f79500"), width=6),
            dbc.Col(dcc.Loading(dcc.Graph(figure=px.imshow(defense_data_corr, x=defense_data_corr.columns, 
                y=defense_data_corr.columns, zmin=-1, zmax=1, color_continuous_scale='RdBu', 
                title="Correlation Heatmap of Defensive Metrics", labels={'color': 'Correlation'})), 
                type="circle", color="#f79500"), width=6),
        ]),
        html.Br(),
        html.Hr(),
        html.Div([
            html.Div([
                #html.H2("Comparison of Goal Scoring Features Among Players", style={'textAlign': 'center'}),
                dcc.Graph(figure=dv.fig_finish_features)
            ], style={'flex': '1', 'margin': '10px'}),
            html.Div([
               # html.H2("Comparison of Shot Features Among Players", style={'textAlign': 'center' , 'font_size': "20px"}),
                dcc.Graph(figure=dv.fig_shot_features)
            ], style={'flex': '1', 'margin': '10px'})
        ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-around'}),
        html.Div([
            html.H1(
                "Top 10 Midfielders: Radar Chart of Attacking Metrics",
                style={'textAlign': 'center', 'marginBottom': '20px'}
            ),
            html.Div([
                html.Div([
                    html.Label("Select a Player:", style={'marginRight': '20px', 'textAlign': 'center'}),
                    dcc.Dropdown(
                        id='player-dropdown',
                        options=[{'label': name, 'value': name} for name in dv.best_midfielder_data['Name']],
                        value=dv.best_midfielder_data['Name'].iloc[0],
                        style={'width': '300px'}
                    )
                ], style={
                    'alignItems': 'center', 
                    'marginRight': '20px'
                }),
                dcc.Graph(
                    id='radar-chart', 
                    style={
                        'width': '500px', 
                        'height': '500px'
                    }
                )
                ], style={
                    'display': 'flex', 
                    'alignItems': 'center',
                    'justifyContent': 'center'
                })
            ], style={'alignItems': 'center'}),
        html.Div([
            html.H1("Top 10 Midfielders: Defensive Metrics Comparison", style={'textAlign': 'center'}),
    
    html.Div([
        html.Label("Select a Metric:", style={'fontSize': '18px'}),
        dcc.Dropdown(
            id='defense-metric-dropdown',
            options=[{'label': feature, 'value': feature} for feature in dv.mid_defense_features],
            value='Tackles', 
            style={'width': '50%', 'margin': 'auto'}
        )
    ], style={'textAlign': 'center', 'padding': '20px'}),
    
    html.Div([
        dcc.Graph(id='defense-bar-chart')
    ]),
    
    html.H1(id="dynamic-heading-top10-Defender", style={'textAlign': 'center'}),
    
    html.Div([
        html.Label("Select a Metric:", style={'fontSize': '18px'}),
        dcc.Dropdown(
            id='metric-dropdown',
            options=[{'label': col, 'value': col} for col in dv.numeric_columns],
            value=dv.numeric_columns[0] if dv.numeric_columns else None,
            style={'width': '50%', 'margin': 'auto'}
        )
    ], style={'textAlign': 'center', 'padding': '20px'}),
    
    html.Div([
        dcc.Graph(id='metric-bar-chart')
    ])
        ])
    ])
], fluid=True)



# callback cards and graphs
@callback(
    [
        Output("age-bar", "figure"),
        Output("age-violin", "figure"),
        Output("over-under-25", "figure"),
        Input("age-bar", "id"),
        Input("age-violin", "id"),
        Input("over-under-25", "id"),
    ],
)
def update_chart(age_bar,age_violin,over_under_25):

    # age_bar
    today = datetime.now() 

    defender_data['Date of Birth'] = pd.to_datetime(defender_data['Date of Birth'], dayfirst=True)
    defender_data['Age'] = today.year - defender_data['Date of Birth'].dt.year

    forward_data['Date of Birth'] = pd.to_datetime(forward_data['Date of Birth'], dayfirst=True)
    forward_data['Age'] = today.year - forward_data['Date of Birth'].dt.year

    goalkeeper_data['Date of Birth'] = pd.to_datetime(goalkeeper_data['Date of Birth'], dayfirst=True)
    goalkeeper_data['Age'] = today.year - goalkeeper_data['Date of Birth'].dt.year

    midfielder_data['Date of Birth'] = pd.to_datetime(midfielder_data['Date of Birth'], dayfirst=True)
    midfielder_data['Age'] = today.year - midfielder_data['Date of Birth'].dt.year

    hist_data = (
        defender_data['Age'].tolist() + 
        forward_data['Age'].tolist() + 
        goalkeeper_data['Age'].tolist() + 
        midfielder_data['Age'].tolist()
    )

    group = ["All Players' Age"]
    fig_age_bar = ff.create_distplot([hist_data], group,bin_size=1, show_rug=False)
    fig_age_bar.update_layout(bargap=0.01, title="Age Distribution of All Players",xaxis_title = 'Age', yaxis_title = 'Percentage',showlegend = False,paper_bgcolor='#DEE0E0',margin=dict(pad=0, r=20, t=50, b=60, l=60))
    fig_age_bar.update_yaxes(
        tickformat=".1%",  # Show percentage format
        title_text="Percentage"
    )

    # age_violin
    df = pd.concat([defender_data, forward_data, goalkeeper_data, midfielder_data],ignore_index=True)
    age_avg=df['Age'].mean()
    fig_age_viloin = px.violin(df, y="Age", x="Position", box=True, title='Players Age distribution by position',template='plotly')
    fig_age_viloin.update_layout(paper_bgcolor='#DEE0E0',margin=dict(pad=0, r=20, t=50, b=60, l=60))
    fig_age_viloin.add_shape(type="line", line_color="blue", line_width=3, opacity=1, line_dash="dot",x0=0, x1=1, xref="paper", y0=age_avg, y1=age_avg, yref="y")

    # over-under-25
    df1 = defender_data[defender_data['Age'] > 25] # dataset for players over 25
    df2 = forward_data[forward_data['Age'] > 25] # dataset for players over 25
    df3 = midfielder_data[midfielder_data['Age'] > 25] # dataset for players over 25
    df4 = defender_data[defender_data['Age'] <= 25] # dataset for players under 25
    df5 = forward_data[forward_data['Age'] <= 25] # dataset for players under 25
    df6 = midfielder_data[midfielder_data['Age'] <= 25] # dataset for players under 25

    df_all_players = pd.concat([df1,df2,df3,df4,df5,df6], ignore_index=True)
    df_all_over_25 = pd.concat([df1,df2,df3] ,ignore_index= True)
    df_all_under_25 = pd.concat([df4, df5, df6], ignore_index=True)

    total_playes = df_all_players.groupby('Club').size()

    x_under_25 = df_all_under_25.groupby('Club').size()
    x_under_25_pro = x_under_25 / total_playes

    x_over_25 = df_all_over_25.groupby('Club').size()
    x_over_25_pro = x_over_25 / total_playes

    y_club_names = np.unique(np.concatenate([defender_data['Club'].unique(),forward_data['Club'].unique(),midfielder_data['Club'].unique()]))

    fig_over_under_25 = go.Figure()

    # Add bars for 'Under 25'
    fig_over_under_25.add_trace(go.Bar(
        x=x_under_25_pro,
        y=y_club_names,
        name='Under 25',
        orientation='h',
        marker=dict(color='#59CAB3', line=dict(color='whitesmoke', width=1.1))
    ))

    # Add bars for 'Over 25'
    fig_over_under_25.add_trace(go.Bar(
        x=x_over_25_pro,
        y=y_club_names,
        name='Over 25',
        orientation='h',
        marker=dict(color='#4D5FB8', line=dict(color='whitesmoke', width=1.1))
    ))

    # Update layout
    fig_over_under_25.update_layout(
        barmode='stack',
        title=dict(
            text="Players over 25 and under 25 years old by club",
            font=dict(size=14)
        ),
        xaxis=dict(title="Proportion"),
        yaxis=dict(title="Club Name", tickfont=dict(size=10)),
        legend=dict(
            title=dict(text="Age of players"),
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="right",
            x=0.95
        ),
        margin=dict(pad=0, r=20, t=125, b=60, l=170),
        height=600,
        width=900,
        paper_bgcolor='#DEE0E0',
    )
    
    return (
        fig_age_bar,
        fig_age_viloin,
        fig_over_under_25,
    )
@app.callback(
    Output('feature-comparison-chart', 'figure'),
    [Input('feature-dropdown', 'value')]
)
def update_feature_chart(selected_feature):
    return dv.update_feature_chart(selected_feature)

@app.callback(
    Output('radar-chart', 'figure'),
    [Input('player-dropdown', 'value')]
)
def update_radar_chart(player_name):
    return dv.update_radar_chart(player_name)

@app.callback(
    Output('defense-bar-chart', 'figure'),
    [Input('defense-metric-dropdown', 'value')]
)
def update_bar_chart_defense(selected_metric):
    return dv.update_bar_chart_defense(selected_metric)

@app.callback(
    Output('metric-bar-chart', 'figure'),
    [Input('metric-dropdown', 'value')]
)
def update_bar_chart_metric(selected_metric):
    return dv.update_bar_chart_metric(selected_metric)
@app.callback(
    Output('dynamic-heading-top10-Defender', 'children'),
    Input('metric-dropdown', 'value')
)
def update_heading(selected_metric):
    if selected_metric:
        return f"Top 10 Defenders by {selected_metric}"
    return "Top 10 Defenders"  # Default heading

if __name__ == '__main__':
    app.run_server(port = '8080')