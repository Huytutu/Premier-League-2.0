from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
import selenium
import matplotlib.pyplot as plt
import dash
import plotly.graph_objects as go
import random
from dash import callback, dcc, html, Output, Input, dash
import dash_bootstrap_components as dbc

# Get data

head_paths = "../../Data"

def redirect(head_path, original = head_paths):# đường dẫn đến data
    original = head_path

file_path = "./Data/Club/all_data_of_clubs.csv"
data = pd.read_csv(file_path)
data.rename(columns={"Unnamed: 0": "Team"}, inplace=True)
midfielder_data = pd.read_csv("./Data/Stats_csv/Processed_Midfielder_data.csv")
forward_data = pd.read_csv("./Data/Stats_csv/Processed_Forward_data.csv")
defender_data = pd.read_csv("./Data/Stats_csv/Processed_Defender_data.csv")


# Prepare attacking data

attacking_features = ['Goals', 'Goals per match', 'Penalties scored', 'Shots', 'Shots on target', 'Big Chances Created', 'Shooting accuracy %']
attacking_data = data[['Team'] + attacking_features]


# Prepare defensive data


defensive_features = ['Clean sheets', 'Goals Conceded', 'Tackles', 'Tackle success %', 'Errors leading to goal', 'Interceptions']
defensive_data = data[['Team'] + defensive_features]


# Prepare prossessing data
control_features = ['Passes', 'Passes per match', 'Pass accuracy %', 'Crosses', 'Cross accuracy %']
control_data = data[['Team'] + control_features]

control_fig = px.bar(
    control_data.melt(id_vars='Team', value_vars=control_features, var_name='Metric', value_name='Value'),
    x='Team', y='Value', color='Metric',
    barmode='group',
    title="Comparison of Control Metrics Across Teams"
)


# Heatmap of Correlations - Attacking Performance
attack_data_corr = data[['Goals', 'Goals per match', 'Penalties scored', 'Shots', 'Shots on target',
                         'Big Chances Created', 'Shooting accuracy %', 'Passes', 'Passes per match',
                         'Pass accuracy %']].corr()

heatmap_data = attack_data_corr.reset_index().melt(id_vars='index')
heatmap_data.columns = ['Feature1', 'Feature2', 'Correlation']

heatmap_fig = px.imshow(
    attack_data_corr,
    x=attack_data_corr.columns,
    y=attack_data_corr.columns,
    zmin=-1, zmax=1,
    color_continuous_scale='RdBu',
    title="Correlation Heatmap of Attack Metrics",
    labels={'color': 'Correlation'}
)
# Heatmap of Correlations - Defensing Performance
defense_data_corr = data[['Clean sheets', 'Goals Conceded', 'Tackles', 'Tackle success %', 'Interceptions', 'Saves',
                          'Blocked shots', 'Clearances', 'Headed Clearance', 'Aerial Battles/Duels Won', 'Own goals',
                          'Passes', 'Passes per match', 'Pass accuracy %']].corr()

defense_heatmap_fig = px.imshow(
    defense_data_corr,
    x=defense_data_corr.columns,
    y=defense_data_corr.columns,
    zmin=-1, zmax=1,
    color_continuous_scale='RdBu',
    title="Correlation Heatmap of Defensive Metrics",
    labels={'color': 'Correlation'}
)


# Top 10 best forward




finish_features = ['Name','Headed goals', 'Goals with right foot', 'Goals with left foot', 'Penalties scored', 'Freekicks scored']
forward_best_score = forward_data.sort_values(by='Goals', ascending=False).head(10)
forward_best_score_features = forward_best_score[finish_features]
fig_finish_features = px.bar(
    forward_best_score_features.melt(id_vars='Name', value_vars=finish_features, var_name='Metrics', value_name='Value'),
    x = 'Name',
    y = 'Value',
    color='Metrics',
    barmode='group',
    title='Comparison of Goal Scoring Features Among Players'
)

shot_features = ['Name', 'Shots', 'Shots on target', 'Shooting accuracy %', 'Hit woodwork', 'Big chances missed']
forward_shot_features = forward_best_score[shot_features]
fig_shot_features = px.bar(
    forward_shot_features.melt(id_vars='Name', value_vars=shot_features, var_name='Metrics', value_name='Value'),
    x = 'Name',
    y = 'Value',
    color = 'Metrics',
    barmode = 'group',
    title= 'Comparison of Shot Features Among Players',
    color_discrete_sequence=['#b70ef1', '#0ed2f1', '#0ef148', '#f1c10e', '#f10e37']
)


# Top 10 best midfielder



best_midfielder_data = midfielder_data.sort_values(by='Assists', ascending=False)
best_midfielder_data['Cross accuracy %'] = (
    best_midfielder_data['Cross accuracy %']
    .str.replace('%', '', regex=False)
    .astype(float)
)
best_midfielder_data['Tackle success %'] = (
    best_midfielder_data['Tackle success %']
    .str.replace('%', '', regex=False)
    .astype(float)
)
best_midfielder_data['Tackle success'] = best_midfielder_data['Tackle success %']*best_midfielder_data['Tackles']/100
available_features = ['Assists', 'Passes', 'Passes per match', 'Big Chances Created',
                      'Crosses', 'Cross accuracy %', 'Through balls', 'Accurate long balls']

mid_attack_features = ['Goals', 'Goals per match', 'Freekicks scored', 'Shots', 'Shots on target', 'Shots on target']
mid_defense_features = ['Tackles', 'Tackle success %', 'Interceptions', 'Duels won']


# Top 10 best defender




defender_data['Tackle success %'] = (
    defender_data['Tackle success %']
    .astype(str)
    .str.replace('%', '', regex=False) 
    .astype(float) 
)
defender_data['Cross accuracy %'] = (
    defender_data['Cross accuracy %']
    .astype(str)
    .str.replace('%', '', regex=False) 
    .astype(float) 
)
numeric_columns = defender_data.select_dtypes(include=['float64', 'int64']).columns.tolist()


# Layout




app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title="Visualization App")

app.layout = html.Div([
    html.H1("Football Clubs Performance Metrics", style={'textAlign': 'center'}),

    html.Div([
        html.H2("Attacking Metrics Trends", style={'textAlign': 'center'}),
        dcc.Graph(
            figure=px.line(
                attacking_data.melt(id_vars='Team', value_vars=attacking_features, var_name='Metric', value_name='Value'),
                x='Team', y='Value', color='Metric',
                title="Attacking Metrics Trends Across Teams"
            )
        )
    ]),

    html.Div([
        html.H2("Defensive Metrics Stacked Bar", style={'textAlign': 'center'}),
        dcc.Graph(
            figure=px.bar(
                defensive_data.melt(id_vars='Team', value_vars=defensive_features, var_name='Metric', value_name='Value'),
                x='Team', y='Value', color='Metric',
                title="Defensive Metrics Distribution Across Teams",
                barmode='stack'
            )
        )
    ]),

    html.Div([
        html.H2("Control Metrics Grouped Bar Chart", style={'textAlign': 'center'}),
        dcc.Graph(figure=control_fig)
    ]),

    html.Div([
        html.H2("Correlation Heatmap of Attack Metrics", style={'textAlign': 'center'}),
        dcc.Graph(figure=heatmap_fig)
    ]),
    html.Div([
        html.H2("Correlation Heatmap of Defensive Metrics", style={'textAlign': 'center'}),
        dcc.Graph(figure=defense_heatmap_fig)
    ]),


    html.Div([
        html.H2("Comparison of Goal Scoring Features Among Players", style={'textAlign': 'center'}),
        dcc.Graph(figure=fig_finish_features)
    ]),
    html.Div([
        html.H2("Comparison of Shot Features Among Players", style={'textAlign': 'center'}),
        dcc.Graph(figure=fig_shot_features)
    ]),

    html.Div([
        html.H2("Top 10 Midfielders: Feature Comparison", style={'textAlign': 'center'}),
        html.Div([
            html.Label("Select a Metric:", style={'fontSize': '18px'}),
            dcc.Dropdown(
                id='feature-dropdown',
                options=[{'label': feature, 'value': feature} for feature in available_features],
                value='Assists',
                style={'width': '50%', 'margin': 'auto'}
            )
        ], style={'textAlign': 'center', 'padding': '20px'}),
        html.Div([
            dcc.Graph(id='feature-comparison-chart')
        ])
    ]),
    
    html.H1("Top 10 Midfielders: Radar Chart of Attacking Metrics", style={'textAlign': 'center'}),
    
    html.Div([
        html.Label("Select a Player:", style={'fontSize': '18px'}),
        dcc.Dropdown(
            id='player-dropdown',
            options=[{'label': name, 'value': name} for name in best_midfielder_data['Name']],
            value=best_midfielder_data['Name'].iloc[0],
            style={'width': '50%', 'margin': 'auto'}
        )
    ], style={'textAlign': 'center', 'padding': '20px'}),
    
    html.Div([
        dcc.Graph(id='radar-chart')
    ]),
    
    html.H1("Top 10 Midfielders: Defensive Metrics Comparison", style={'textAlign': 'center'}),
    
    html.Div([
        html.Label("Select a Metric:", style={'fontSize': '18px'}),
        dcc.Dropdown(
            id='metric-dropdown',
            options=[{'label': feature, 'value': feature} for feature in mid_defense_features],
            value='Tackles', 
            style={'width': '50%', 'margin': 'auto'}
        )
    ], style={'textAlign': 'center', 'padding': '20px'}),
    
    html.Div([
        dcc.Graph(id='defense-bar-chart')
    ]),
    
    html.H1("Top 10 Defender by Selected Metric", style={'textAlign': 'center'}),
    
    html.Div([
        html.Label("Select a Metric:", style={'fontSize': '18px'}),
        dcc.Dropdown(
            id='metric-dropdown',
            options=[{'label': col, 'value': col} for col in numeric_columns],
            value=numeric_columns[0] if numeric_columns else None,
            style={'width': '50%', 'margin': 'auto'}
        )
    ], style={'textAlign': 'center', 'padding': '20px'}),
    
    html.Div([
        dcc.Graph(id='metric-bar-chart')
    ])

])

@app.callback(
    Output('feature-comparison-chart', 'figure'),
    [Input('feature-dropdown', 'value')]
)
def update_feature_chart(selected_feature):
    color_sequence = px.colors.qualitative.Plotly
    random.shuffle(color_sequence)
    fig = px.bar(
        best_midfielder_data.head(10),
        x='Name',
        y=selected_feature,
        title=f"Comparison of {selected_feature} for Top 10 Players",
        text=selected_feature,
        color_discrete_sequence=color_sequence
    )
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(yaxis_title='Value', xaxis_title='Player', template='plotly_white')
    return fig

@app.callback(
    Output('radar-chart', 'figure'),
    [Input('player-dropdown', 'value')]
)
def update_radar_chart(player_name):
    player_stats = best_midfielder_data[best_midfielder_data['Name'] == player_name][mid_attack_features].iloc[0]
    values = player_stats.tolist()
    values += values[:1]

    radar_chart = go.Figure()
    radar_chart.add_trace(go.Scatterpolar(
        r=values,
        theta=mid_attack_features + [mid_attack_features[0]], 
        fill='toself',
        name=player_name
    ))
    radar_chart.update_layout(
        polar=dict(
            radialaxis=dict(visible=True),
        ),
        title=f"Radar Chart for {player_name}",
        title_x = 0.5,
        showlegend=False,
        width=500,  # Set the width of the chart
        height=500  # Set the height of the chart
    )
    return radar_chart

@app.callback(
    Output('defense-bar-chart', 'figure'),
    [Input('metric-dropdown', 'value')]
)
def update_bar_chart_defense(selected_metric):
    if(selected_metric=='Tackle success %'):
        data = best_midfielder_data.sort_values(by='Tackle success', ascending=False).head(10)
    else:
        data = best_midfielder_data.sort_values(by=selected_metric, ascending=False).head(10)
    color_sequence = px.colors.qualitative.Plotly
    random.shuffle(color_sequence)
    
    fig = px.bar(
        data,
        x='Name', 
        y=selected_metric, 
        title=f"Comparison of {selected_metric} for Top 10 Players",
        text=selected_metric, 
        labels={'Name': 'Player', selected_metric: 'Value'},
        color_discrete_sequence=color_sequence
    )
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(yaxis_title='Value', xaxis_title='Player', template='plotly_white')
    return fig

@app.callback(
    Output('metric-bar-chart', 'figure'),
    [Input('metric-dropdown', 'value')]
)
def update_bar_chart_metric(selected_metric):
    top_10_data = defender_data.nlargest(10, selected_metric)
    color_sequence = px.colors.qualitative.Plotly
    random.shuffle(color_sequence)
    
    fig = px.bar(
        top_10_data,
        x='Name', 
        y=selected_metric, 
        title=f"Top 10 Players by {selected_metric}",
        text=selected_metric,
        labels={'Name': 'Player', selected_metric: 'Value'},
        color_discrete_sequence=color_sequence
    )
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(yaxis_title='Value', xaxis_title='Player', template='plotly_white')
    return fig

#app.run_server(debug=True)