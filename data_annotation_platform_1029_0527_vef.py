# 代码生成时间: 2025-10-29 05:27:59
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate

# 定义Dash应用程序
app = dash.Dash(__name__)

# 定义布局
app.layout = html.Div(children=[
    html.H1("数据标注平台"),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['点击上传', html.A('选择文件')]),
        description='',
        multiple=True
    ),
    html.Div(id='output-data-upload'),
    dcc.Graph(id='annotation-graph')
])

# 回调函数：上传文件后处理数据并更新图表
@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')]
)
def update_output(uploaded_contents):
    if uploaded_contents is None:
        raise PreventUpdate
    return html.Div([
        html.H5('文件名：'),
        html.P(uploaded_contents.filename),
        html.H5('文件大小：'),
        html.P(f'{len(uploaded_contents)} bytes')
    ])

# 回调函数：上传文件后更新图表
@app.callback(
    Output('annotation-graph', 'figure'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_graph(uploaded_contents, filename):
    if uploaded_contents is None:
        raise PreventUpdate
    # 读取数据
    try:
        df = pd.read_csv(uploaded_contents)
    except Exception as e:
        print(f'读取文件失败：{e}')
        raise PreventUpdate
    # 根据数据生成图表
    fig = px.histogram(df, x=df.columns[0], title='数据标注图表')
    return fig

# 运行服务器
if __name__ == '__main__':
    app.run_server(debug=True)