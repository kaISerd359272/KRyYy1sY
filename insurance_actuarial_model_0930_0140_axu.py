# 代码生成时间: 2025-09-30 01:40:27
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import norm

# 初始化 Dash 应用
app = dash.Dash(__name__)

# 定义页面布局
app.layout = html.Div([
    html.H1("Insurance Actuarial Model"),
    dcc.Markdown("""
    ### Model Parameters
    Fill out the form to calculate actuarial data.
    """),
    html.Div([
        dcc.Input(id='age', type='number', placeholder='Enter age', min=0, required=True),
        dcc.Input(id='annual_premium', type='number', placeholder='Enter annual premium', min=0, required=True),
        dcc.Input(id='years', type='number', placeholder='Enter years', min=1, required=True),
    ]),
    html.Div(id='output-container'),
])

# 定义辅助函数：计算精算数据
def calculate_actuarial_data(age, annual_premium, years):
    """
    Calculate actuarial data based on age, annual premium, and years.

    Args:
    age (int): The age of the insured.
    annual_premium (float): The annual premium paid by the insured.
    years (int): The number of years for which the premium is paid.

    Returns:
    dict: A dictionary containing actuarial data.
    """
    try:
        # 计算累积保费
        cumulative_premium = annual_premium * years

        # 假设精算模型为简单的指数增长模型
        # 这里使用正态分布模拟生命表，实际模型可能更复杂
        survival_rate = norm.cdf(age + years, loc=70, scale=10)

        # 计算预期赔付金额
        expected_payout = cumulative_premium * survival_rate

        return {
            'cumulative_premium': cumulative_premium,
            'expected_payout': expected_payout,
            'survival_rate': survival_rate
        }
    except Exception as e:
        # 错误处理
        print(f"Error calculating actuarial data: {e}")
        return {
            'cumulative_premium': None,
            'expected_payout': None,
            'survival_rate': None
        }

# 定义回调函数：当输入参数变化时更新输出
@app.callback(
    Output('output-container', 'children'),
    [Input('age', 'value'), Input('annual_premium', 'value'), Input('years', 'value')],
    prevent_initial_call=True
)
def update_output(age, annual_premium, years):
    """
    Update the output container when input parameters change.

    Args:
    age (int): The age of the insured.
    annual_premium (float): The annual premium paid by the insured.
    years (int): The number of years for which the premium is paid.

    Returns:
    str: A string containing the updated actuarial data.
    """
    if age is None or annual_premium is None or years is None:
        return "Please fill out all input fields."

    actuarial_data = calculate_actuarial_data(age, annual_premium, years)

    return html.Div([
        html.H2("Actuarial Data"),
        html.P(f"Cumulative Premium: {actuarial_data['cumulative_premium']}"),
        html.P(f"Expected Payout: {actuarial_data['expected_payout']:.2f}"),
        html.P(f"Survival Rate: {actuarial_data['survival_rate']:.2%}"),
    ])

# 运行 Dash 应用
if __name__ == '__main__':
    app.run_server(debug=True)