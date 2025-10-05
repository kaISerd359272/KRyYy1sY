# 代码生成时间: 2025-10-05 17:04:42
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd

# 初始化Dash应用
app = dash.Dash(__name__)

# 应用布局
app.layout = html.Div([
    html.H1("DeFi协议实现"),
    dcc.Graph(id='crypto-chart'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    ),
])

# 模拟DeFi数据
def generate_ethereum_price():
    # 这里可以替换为实际获取DeFi数据的逻辑
    return {"price": round(100 + 10*pd.np.random.randn(), 2)}

# 回调函数更新图表数据
@app.callback(
    Output('crypto-chart', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph_live(n):  # n 是interval-component触发的次数
    df = pd.DataFrame([generate_ethereum_price()], columns=['price'])
    fig = px.line(df, x=df.index, y='price', title='Ethereum Price Over Time')
    return fig

# 运行服务器
if __name__ == '__main__':
    app.run_server(debug=True)