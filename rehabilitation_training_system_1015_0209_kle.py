# 代码生成时间: 2025-10-15 02:09:30
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
from flask import session
from datetime import datetime

# 定义康复训练系统应用
app = dash.Dash(__name__)
app.title = '康复训练系统'

# 加载数据
df = pd.read_csv('data/rehabilitation_data.csv')

# 定义应用布局
app.layout = html.Div(children=[
    html.H1(children='康复训练系统'),
    html.Div(children='', id='output-container'),
    dcc.Graph(id='rehabilitation-graph'),
    dcc.Dropdown(
        id='rehabilitation-dropdown',
        options=[{'label': i, 'value': i} for i in df['PatientID'].unique()],
        value=df['PatientID'].unique()[0],
        multi=False
    ),
    dcc.DatePickerRange(
        id='rehabilitation-date-picker',
        min_date_allowed=date(2020, 1, 1),
        max_date_allowed=datetime.today().date(),
        start_date=datetime.today().date() - timedelta(days=7),
        end_date=datetime.today().date(),
        display_format='YYYY-MM-DD'
    )
])

# 定义回调函数，更新图表
@app.callback(
    Output('rehabilitation-graph', 'figure'),
    Input('rehabilitation-dropdown', 'value'),
    Input('rehabilitation-date-picker', 'start_date'),
    Input('rehabilitation-date-picker', 'end_date')
)
def update_rehabilitation_graph(patient_id, start_date, end_date):
    # 筛选数据
    filtered_df = df[(df['PatientID'] == patient_id) &
                    (df['Date'] >= start_date) &
                    (df['Date'] <= end_date)]
    
    # 如果没有数据，显示空图
    if filtered_df.empty:
        raise PreventUpdate

    # 绘制图表
    fig = px.line(filtered_df, x='Date', y='TrainingScore', title=f'患者{patient_id}康复训练得分')
    return fig

# 定义错误处理回调函数
@app.callback(Output('output-container', 'children'),
              Exception('value', 'consolidated'), State('output-container', 'children'))
def handle_exception(context, output_container):
    # 输出错误信息
    output_container = [html.Div([f'发生错误: {context}'])]
    return output_container

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)