import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as go

df1 = pd.read_csv('Data/calories.csv')

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='EatWell',
            style={
                'textAlign': 'center',
                'color': '#104c31'
            }),
    html.Div('Enter your daily diet to see a number of nutritional graphs ', style={'textAlign': 'center'}),
    html.Div('Have you ever been curious how many calories you eat daily? Or how much energy is gained from your current diet?', style={'textAlign': 'center'}),
    html.Div('Use the EatWell Calculator to find the answers to these questions'),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#c1af6c'}),
    html.H3('Calculator Requirements:', style={'textAlign': 'center'}),
    html.P('Put each food on a new line', style={'textAlign': 'center'}),
    html.P('Capitalize every word', style={'textAlign': 'center'}),
    html.P('Generalize, "McDonalds Cheeseburger" will not work, but "Cheeseburge" will work correctly', style={'textAlign': 'center'}),
    html.H4('Example Input Below:', style={'textAlign': 'center'}),
    html.P('Pepperoni Pizza', style={'textAlign': 'center'}),
    html.P('Apple', style={'textAlign': 'center'}),
    html.P('Cheeseburger', style={'textAlign': 'center'}),
    html.P('Diet Coke', style={'textAlign': 'center'}),
    dcc.Textarea(id='food-input', style={'width': '50%', 'height': 100}),
    html.H3('Calorie Pie Chart', style={'color': '#104c31', 'textAlign': 'center'}),
    html.P('Use this chart to determine what percentage of your daily calorie intake each food item is', style={'textAlign': 'center'}),
    html.P('Note that while more calories are not always negative, having a high % of calories in one item can be unhealthy', style={'textAlign': 'center'}),
    dcc.Graph(id='calorie-pie'),
    html.H3('Energy Pie Chart', style={'color': '#104c31', 'textAlign': 'center'}),
    html.P('Depending on your location, you may use kilojoules instead of calories to measure energy from food', style={'textAlign': 'center'}),
    dcc.Graph(id='energy-pie'),
    html.H3('Top 10 Calorie Heavy Foods', style={'color': '#104c31', 'textAlign': 'center'}),
    html.P('We looked at over 1000 foods to determine which ones have the highest calorie intake', style={'textAlign': 'center'}),
    html.P('Notice any similarities between these foods?', style={'textAlign': 'center'}),
    dcc.Graph(id='calorie-top-10'),
    html.H3('Food Bubble Chart', style={'color': '#104c31', 'textAlign': 'center'}),
    html.P('Energy gained from over 1000 foods in our datasets visualized via bubble chart', style={'textAlign': 'center'}),
    html.P('Hover over any bubble to view its information', style={'textAlign': 'center'}),
    html.P('Additionally, use the side legend to filter out categories of food', style={'textAlign': 'center'}),
    dcc.Graph(id='food-bubble')

], style={'textAlign': 'center'})


@app.callback(Output('calorie-pie', 'figure'),
              Input('food-input', 'value'))
def calories(food_list):
    food_list = food_list.split('\n')
    df1 = pd.read_csv('Data/calories.csv')

    filtered_df = df1[df1['FoodItem'].isin(food_list)]

    # print(filtered_df)

    filtered_df = filtered_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    fig = go.pie(filtered_df, values='Cals_per100grams', names='FoodItem')
    return fig


@app.callback(Output('energy-pie', 'figure'),
              Input('food-input', 'value'))
def energy(food_list):
    food_list = food_list.split('\n')
    df1 = pd.read_csv('Data/calories.csv')
    filtered_df = df1[df1['FoodItem'].isin(food_list)]
    filtered_df = filtered_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    fig = go.pie(filtered_df, values='KJ_per100grams', names='FoodItem')
    return fig


@app.callback(Output('calorie-top-10', 'figure'),
              Input('food-input', 'value'))
def calorie_top_10(food_list):
    df1 = pd.read_csv('Data/calories.csv')
    df1 = df1.head(1000)
    sorted_df = df1.sort_values(['Cals_per100grams'], ascending=False).head(10)
    fig = go.bar(sorted_df, x='FoodItem', y='Cals_per100grams')
    return fig


@app.callback(Output('food-bubble', 'figure'),
              Input('food-input', 'value'))
def bubble_chart(food_list):
    df1 = pd.read_csv('Data/calories.csv')
    df1 = df1.head(1000)
    fig = go.scatter(df1, x='Cals_per100grams', y='KJ_per100grams', size='Cals_per100grams', color='FoodCategory', hover_name='FoodItem')
    return fig


if __name__ == '__main__':
    app.run_server()
