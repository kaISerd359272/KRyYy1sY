# 代码生成时间: 2025-10-07 23:48:34
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import json
import pandas as pd

# 初始化Dash应用
app = dash.Dash(__name__)

# 定义应用布局
app.layout = html.Div([
    # 标题
    html.H1('JSON 数据格式转换器'),
    # 输入框，用于输入JSON数据
    dcc.Textarea(id='input-json', value='{}', style={'width': '100%', 'height': '200px'}),
    # 选择按钮，用于选择转换类型
    html.Button('转换为DataFrame', id='convert-button', n_clicks=0),
    # 输出框，用于显示转换结果
    dcc.Textarea(id='output', style={'width': '100%', 'height': '200px'}),
])

# 定义回调函数，用于处理按钮点击事件
@app.callback(
    Output('output', 'value'),
    [Input('convert-button', 'n_clicks')],
    [State('input-json', 'value'), State('output', 'value')],
)
def convert_to_dataframe(n_clicks, input_json, output):
    # 检查输入框是否为空
    if not input_json or n_clicks == 0:
        return ''
    try:
        # 加载JSON数据
        json_data = json.loads(input_json)
        # 将JSON数据转换为DataFrame
        df = pd.json_normalize(json_data)
        # 将DataFrame转换为字符串形式，以便输出
        output_df = df.to_string()
        return output_df
    except json.JSONDecodeError as e:
        # 处理JSON解析错误
        return f'JSON解析错误：{e}'
    except Exception as e:
        # 处理其他异常
        return f'转换错误：{e}'

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)