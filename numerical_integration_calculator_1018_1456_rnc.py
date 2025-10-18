# 代码生成时间: 2025-10-18 14:56:15
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import scipy.integrate as spi
from functools import wraps
import numpy as np

# 函数装饰器，用于错误处理
def error_handling(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return str(e)
    return wrapper

# 数值积分函数
@error_handling
def numerical_integration(f, a, b):
    """Perform numerical integration using scipy.integrate.quad.

    Args:
        f (callable): The function to integrate, f(x).
        a (float): The lower limit of integration.
        b (float): The upper limit of integration.

    Returns:
        float: The estimated value of the definite integral.
    """
    result, error = spi.quad(f, a, b)
    return result

# 创建Dash应用
app = dash.Dash(__name__)

# 应用布局
app.layout = html.Div([
    html.H1("Numerical Integration Calculator"),
    dcc.Dropdown(
        id='function-dropdown',
        options=[
            {'label': 'x^2', 'value': 'x**2'},
            {'label': 'sin(x)', 'value': 'np.sin(x)'},
            {'label': 'exp(-x)', 'value': 'np.exp(-x)'},
        ],
        value='x**2',
    ),
    html.Div(id='function-display'),
    dcc.Slider(
        id='a-slider',
        min=-10,
        max=10,
        value=-1,
        step=1,
        marks={str(i): str(i) for i in range(-10, 11)},
    ),
    dcc.Slider(
        id='b-slider',
        min=-10,
        max=10,
        value=1,
        step=1,
        marks={str(i): str(i) for i in range(-10, 11)},
    ),
    html.Button('Integrate', id='integrate-button', n_clicks=0),
    html.Div(id='result'),
])

# 更新函数显示
@app.callback(
    Output('function-display', 'children'),
    [Input('function-dropdown', 'value')]
)
def update_function_display(selected_option):
    """Update the function display based on the selected dropdown option."""
    return f'f(x) = {selected_option}'

# 计算积分
@app.callback(
    Output('result', 'children'),
    [Input('integrate-button', 'n_clicks'),
     Input('a-slider', 'value'),
     Input('b-slider', 'value'),
     Input('function-dropdown', 'value')],
    [State('function-dropdown', 'value')]
)
def integrate(n_clicks, a, b, func):
    """Perform numerical integration and update the result."""
    if n_clicks == 0:
        return ''
    
    # 将选中的函数字符串转换为可调用函数
    function = eval(f'lambda x: {func}')
    
    # 执行数值积分
    result = numerical_integration(function, a, b)
    
    return f'Integral result: {result:.4f}'

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)