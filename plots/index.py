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
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#c1af6c'}),
    html.Div('Example Input Below:', style={'textAlign': 'center'}),
    dcc.Textarea(id='food-input', value='Apple\nPepperoni Pizza\nDiet Coke',
                 style={'width': '50%', 'height': 100}),
    html.H3('Calorie Pie Chart', style={'color': '#104c31', 'textAlign': 'center'}),
    dcc.Graph(id='calorie-pie'),
    html.H3('Energy Pie Chart', style={'color': '#104c31', 'textAlign': 'center'}),
    dcc.Graph(id='energy-pie'),
    html.H3('Top 10 Calorie Heavy Foods', style={'color': '#104c31', 'textAlign': 'center'}),
    dcc.Graph(id='calorie-top-10'),
    html.H3('Bubble Chart', style={'color': '#104c31', 'textAlign': 'center'}),
    dcc.Graph(id='calorie-bottom-10')

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
    sorted_df = df1.sort_values(['Cals_per100grams'], ascending=False).head(10)
    fig = go.bar(sorted_df, x='FoodItem', y='Cals_per100grams')
    return fig


@app.callback(Output('calorie-bottom-10', 'figure'),
              Input('food-input', 'value'))
def bubble_chart(food_list):
    df1 = pd.read_csv('Data/calories.csv')
    df1 = df1.head(1000)
    fig = go.scatter(df1, x='Cals_per100grams', y='KJ_per100grams', size='Cals_per100grams', color='FoodCategory', hover_name='FoodItem')
    return fig


if __name__ == '__main__':
    app.run_server()
