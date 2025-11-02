# 代码生成时间: 2025-11-02 22:17:43
import os
import shutil
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import datetime
import zipfile

# 设置应用程序的基本配置
app = Dash(__name__)
app.title = 'Data Backup and Restore'

# 设定备份和恢复的路径
BACKUP_DIR = 'backup_files'
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# 备份文件的函数
def backup_database():
    """
    备份数据库文件到指定的备份目录
    """
    try:
        backup_name = f'backup_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.zip'
        backup_path = os.path.join(BACKUP_DIR, backup_name)
        with zipfile.ZipFile(backup_path, 'w') as zipf:
            # 假设数据库文件为db.sqlite，可以根据实际文件类型和名称进行修改
            zipf.write('db.sqlite', arcname='db.sqlite')
        return backup_path
    except Exception as e:
        print(f'An error occurred while backing up: {e}')
        return None

# 恢复文件的函数
def restore_database(backup_path):
    """
    从指定的备份文件中恢复数据库
    """
    try:
        with zipfile.ZipFile(backup_path, 'r') as zipf:
            zipf.extractall()
            return True
    except Exception as e:
        print(f'An error occurred while restoring: {e}')
        return False

# 定义Dash组件
app.layout = html.Div([
    html.H1('Data Backup and Restore Application'),
    html.Button('Backup Database', id='backup-button'),
    html.Div(id='backup-output'),
    html.Button('Restore Database', id='restore-button'),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', html.A('Select File')]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False  # 只允许上传一个文件
    ),
    html.Div(id='restore-output')
])

# 回调函数：备份数据库
@app.callback(
    Output('backup-output', 'children'),
    [Input('backup-button', 'n_clicks')],
    prevent_initial_call=True
)
def backup_database_callback(n_clicks):
    if n_clicks and n_clicks > 0:
        backup_file = backup_database()
        if backup_file:
            return f'Backup successful: {backup_file}'
        else:
            return 'Backup failed'
    return None

# 回调函数：上传文件并恢复数据库
@app.callback(
    Output('restore-output', 'children'),
    [Input('upload-data', 'contents'), Input('upload-data', 'filename')],
    prevent_initial_call=True
)
def restore_database_callback(contents, filename):
    if contents is not None:
        file_name, file_extension = os.path.splitext(filename)
        if file_extension == '.zip':
            return restore_database(contents)
        else:
            return 'Unsupported file format'
    return None

# 运行服务器
if __name__ == '__main__':
    app.run_server(debug=True)