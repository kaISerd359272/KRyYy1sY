# 代码生成时间: 2025-10-26 07:02:57
import os
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


# 磁盘空间管理工具
class DiskSpaceManager:
    def __init__(self):
        # 定义 Dash 应用
        self.app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.app.layout = html.Div([
            dbc.Container(
                style={'margin': '20px'},
                children=[
                    html.H1('磁盘空间管理工具'),
                    dcc.Graph(id='disk-space-graph'),
                    html.Button('刷新数据', id='refresh-data-btn', n_clicks=0),
                ]
            )
        ])

        # 定义回调函数
        self.app.callback(
            Output('disk-space-graph', 'figure'),
            [Input('refresh-data-btn', 'n_clicks')],
        )(self.update_disk_space_graph)

    def get_disk_space_info(self):
        """获取磁盘空间信息"""
        total, used, free = shutil.disk_usage('/')
        return {
            'total': total,
            'used': used,
            'free': free,
        }

    def update_disk_space_graph(self, n_clicks):
        """更新磁盘空间图表"""
        if n_clicks is None or n_clicks == 0:
            return {}

        disk_space_info = self.get_disk_space_info()
        total = disk_space_info['total']
        used = disk_space_info['used']
        free = disk_space_info['free']

        # 创建图表数据
        data = [
            {'label': '已用', 'value': used},
            {'label': '可用', 'value': free},
        ]

        # 创建图表配置
        layout = {
            'title': '磁盘空间使用情况',
            'labels': {'pie': '磁盘空间使用情况'}
        }

        return {
            'data': [{'values': [used, free], 'type': 'pie', 'name': '磁盘空间'}],
            'layout': layout,
        }

    def run(self):
        "