# 代码生成时间: 2025-10-10 22:12:06
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate

# 定义全局变量
DATA_URL = 'https://raw.githubusercontent.com/plotly/datasets/master/healthcare.csv'


# 初始化DASH应用
app = dash.Dash(__name__, meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}])

# 应用布局
app.layout = html.Div([
    html.H1('医疗质量监控'),
    dcc.Dropdown(
        id='indicator-dropdown',
        options=[{'label': i, 'value': i} for i in ['Expenditure', 'Life Expectancy', 'Alcohol']],
        value=['Expenditure'],
        multi=True,
    ),
    dcc.Graph(id='indicator-graphic'),
    dcc.Slider(
        id='year-slider',
        min=1960,
        max=2012,
        step=1,
        marks={str(year): str(year) for year in range(1960, 2013)},
        value=1960,
    ),
])

# 回调函数：更新图表
@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('indicator-dropdown', 'value'), Input('year-slider', 'value')],
)
def update_graph(selected_indicators, year):
    # 加载数据
    df = pd.read_csv(DATA_URL)
    df = df[df['Year'] == year]

    # 检查选择的指标是否为空
    if not selected_indicators:
        raise PreventUpdate

    # 构建图表
    figure = px.bar(df, y=selected_indicators, x='Country', text='Country',
                      animation_frame='Year', animation_group='Country',
                      title=f'医疗质量指标：{year}')
    figure.update_layout(title_x=0.5)
    figure.update_yaxes(title_text=selected_indicators)
    return figure

# 运行DASH应用
if __name__ == '__main__':
    app.run_server(debug=True)
