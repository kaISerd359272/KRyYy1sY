# 代码生成时间: 2025-10-02 00:00:30
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

# Inventory management app layout
app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.H1(children='Inventory Management'),
    dcc.Input(id='item-name', type='text', placeholder='Enter item name'),
    dcc.Input(id='item-quantity', type='number', placeholder='Enter quantity'),
    html.Button('Add Item', id='add-item', n_clicks=0),
    dcc.Store(id='inventory-store'),
    html.Div(id='inventory-display')
])

# Callback to add items to the inventory store
@app.callback(
    Output('inventory-store', 'data'),
    [Input('add-item', 'n_clicks')],
    [State('item-name', 'value'), State('item-quantity', 'value'), State('inventory-store', 'data')]
)
def add_item(n_clicks, item_name, item_quantity, inventory_data):
    if n_clicks > 0:  # Check if the button was clicked
        try:  # Error handling for invalid data
            item_quantity = int(item_quantity)
            if inventory_data:  # Append to existing inventory
                inventory_data[item_name] = item_quantity
            else:  # Create new inventory
                inventory_data = {item_name: item_quantity}
            return inventory_data
        except ValueError:  # Handle invalid quantity
            return {"error": "Invalid quantity. Please enter a valid number."}
    return inventory_data

# Callback to display inventory
@app.callback(
    Output('inventory-display', 'children'),
    [Input('inventory-store', 'data')],
    [State('inventory-store', 'data')]
)
def display_inventory(inventory_data):  # Display inventory data
    if inventory_data:  # Check if inventory data exists
        # Generate a table to display inventory
        table = html.Table(
            [html.Thead(html.Tr([html.Th('Item Name'), html.Th('Quantity')])),
             html.Tbody([html.Tr([html.Td(k), html.Td(str(v))]) for k, v in inventory_data.items()])])
        return table
    else:
        return 'No items in inventory.'

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)