# 代码生成时间: 2025-09-23 16:41:45
import os
import shutil
import logging
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# 配置日志
logging.basicConfig(level=logging.INFO)

# 定义文件备份和同步工具类
class BackupSyncTool:
    def __init__(self, source_dir, backup_dir):
        """初始化文件备份和同步工具类
        
        Args:
            source_dir (str): 源目录路径
            backup_dir (str): 备份目录路径
        """
        self.source_dir = source_dir
        self.backup_dir = backup_dir
        self.backup_files = []

    def backup_files(self):
        """备份文件
        """
        for root, dirs, files in os.walk(self.source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                backup_path = os.path.join(self.backup_dir, os.path.relpath(file_path, self.source_dir))
                os.makedirs(os.path.dirname(backup_path), exist_ok=True)
                shutil.copy2(file_path, backup_path)
                self.backup_files.append(backup_path)

    def sync_files(self):
        """同步文件
        """
        for file in self.backup_files:
            file_dir, file_name = os.path.split(file)
            src_file_path = os.path.join(self.source_dir, os.path.relpath(file_dir, self.backup_dir))
            src_file_path = os.path.join(src_file_path, file_name)
            if os.path.exists(src_file_path):
                shutil.copy2(src_file_path, file)
            else:
                logging.warning(f"文件 {src_file_path} 不存在，跳过同步")

# 创建 Dash 应用
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 定义布局
app.layout = html.Div([
    html.H1("文件备份和同步工具"),
    dbc.Alert(
        "请选择源目录和备份目录，然后点击备份和同步按钮",
        color="primary"
    ),
    dbc.Form([
        dbc.FormGroup(
            [
                dbc.Label("源目录"),
                dbc.Input(id="source_dir", placeholder="请输入源目录路径"),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("备份目录"),
                dbc.Input(id="backup_dir", placeholder="请输入备份目录路径"),
            ]
        ),
        dbc.Button("备份文件", id="backup_btn", color="primary"),
        dbc.Button("同步文件", id=