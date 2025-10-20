# 代码生成时间: 2025-10-20 15:42:02
import dash
import dash_core_components as dcc
# NOTE: 重要实现细节
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
# 改进用户体验

"""
A responsive dashboard using the Dash framework.
This dashboard changes layout based on the screen size,
providing an optimal viewing experience.
"""

# Initialize the Dash application
app = dash.Dash(__name__)

# Define the layout of the app
# NOTE: 重要实现细节
app.layout = html.Div(
    [
        # Use a responsive grid layout
        html.Div(
            [
                # Card with a plot
# 改进用户体验
                html.Div(
                    [
# 优化算法效率
                        html.H4("Responsive Plot"),
                        dcc.Graph(id="responsive-plot"),
                    ],
                    className="six columns"
                ),
                # Card with a table
                html.Div(
                    [
# 扩展功能模块
                        html.H4("Responsive Table"),
                        dcc.Table(id="responsive-table"),
# 改进用户体验
                    ],
                    className="six columns"
                ),
# NOTE: 重要实现细节
            ],
            # Responsive grid layout properties
            className="row"
        ),
    ],
    # Responsive layout properties
    style={"display": "flex", "flexDirection": "column", "alignItems": "center"}
)

# Add a callback to update the layout based on the screen size
@app.callback(
    Output("responsive-plot", "figure"),
    [Input("responsive-table", "active_cell")],
    [State("responsive-table", "data"), State("responsive-table", "columns")]
)
def update_plot(active_cell, table_data, table_columns):
    # Error handling for no active cell
    if not active_cell:
        return px.line(x=["No active cell"], y=[0])

    # Extract the column name from the active cell
    column_name = table_columns[active_cell[0, 0]].id

    # Generate a plotly figure based on the selected column
    df = px.data.gapminder().query(f"{column_name}=='{active_cell[0, 1]}'")
    fig = px.line(df, x='year', y=column_name)
    return fig

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)