# 代码生成时间: 2025-10-04 01:34:23
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib
import pandas as pd
import numpy as np
import traceback

def load_data():
    # Load dataset
    iris = load_iris()
    X, y = iris.data, iris.target
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train, y_train):  # 随机森林分类器
    try:
        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        print(traceback.format_exc())
        return None

def app_layout():
    # App layout
    return html.Div(children=[
        html.H1(children='Model Training Monitor'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
    ])

def update_graph_live(input_df):
    # Update graph live function
    y_pred = model.predict(input_df)
    y_true = input_df['y']
    accuracy = np.mean(y_pred == y_true)
    return go.Scatter(
        x=input_df.index,
        y=accuracy,
        mode='lines+markers',
        visible=True
    )
app = dash.Dash(__name__)
app.layout = app_layout()
X_train, X_test, y_train, y_test = load_data()
model = train_model(X_train, y_train)

@app.callback(
    Output('live-update-graph', 'figure'),
    [Input('interval-component', 'n_intervals')],
    [State('live-update-graph', 'figure')]
)
def update_graph_live_callback(n, figure):  # Update graph live callback
    if model is None:  # Check if model is trained
        raise PreventUpdate()
    input_df = pd.DataFrame(X_test, columns=iris.feature_names)
    input_df['y'] = y_test
    return {'data': [update_graph_live(input_df)], 'layout': go.Layout(title='Accuracy over Time')}

if __name__ == '__main__':
    app.run_server(debug=True)