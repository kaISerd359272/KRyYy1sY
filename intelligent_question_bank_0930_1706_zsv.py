# 代码生成时间: 2025-09-30 17:06:58
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pandas as pd
from sqlalchemy import create_engine
import sqlite3

# 数据库配置
DATABASE_URI = 'sqlite:///intelligent_question_bank.db'

# 初始化Dash应用
app = dash.Dash(__name__,
                 external_stylesheets=[dbc.themes.BOOTSTRAP])

# 定义布局
app.layout = dbc.Container(
    children=[
        dbc.Row([dbc.Col(html.H1("智能题库系统"), md=12)]),
        dbc.Row([dbc.Col(dcc.Dropdown(
            id='subject-dropdown',
            options=[{'label': '数学', 'value': 'math'},
                     {'label': '物理', 'value': 'physics'},
                     {'label': '化学', 'value': 'chemistry'}],
            value='math',
            style={'width': '100%'}
        ), md=12)]),
        dbc.Row([dbc.Col(dcc.Dropdown(
            id='difficulty-dropdown',
            options=[{'label': '简单', 'value': 'easy'},
                     {'label': '中等', 'value': 'medium'},
                     {'label': '困难', 'value': 'hard'}],
            value='easy',
            style={'width': '100%'}
        ), md=12)]),
        dbc.Row([dbc.Col(dcc.Textarea(
            id='question-text',
            placeholder='题目内容显示在这里',
            readOnly=True,
            style={'width': '100%', 'height': '200px'}
        ), md=12)]),
    ]
)

# 定义回调函数，根据科目和难度选择题目
@app.callback(
    Output('question-text', 'value'),
    [Input('subject-dropdown', 'value'),
     Input('difficulty-dropdown', 'value')]
)
def get_question(subject, difficulty):
    try:
        # 连接数据库
        engine = create_engine(DATABASE_URI)
        conn = engine.connect()
        
        # 执行查询
        sql = f"SELECT question FROM questions WHERE subject='{subject}' AND difficulty='{difficulty}'"
        result = conn.execute(sql).fetchone()
        
        # 关闭连接
        conn.close()
        
        # 返回题目内容
        if result:
            return result[0]
        else:
            raise PreventUpdate
    except Exception as e:
        # 异常处理
        print(f"Error: {e}")
        raise PreventUpdate

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)