import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from fractions import Fraction

app = dash.Dash(__name__)

def convert_fraction_to_decimal(fraction_string):
    try:
        fraction = Fraction(fraction_string)
        return float(fraction)
    except ValueError:
        return None

def normalize_values(values):
    min_val = min(values)
    max_val = max(values)
    normalized_values = (values - min_val) / (max_val - min_val)
    return normalized_values

# Read CSV file into a DataFrame
csv_filename = "path_data.csv"  # Replace with the actual CSV file path
df = pd.read_csv(csv_filename)

# Convert latitude and longitude from fractions to decimals
df['Latitude'] = df['Latitude'].apply(convert_fraction_to_decimal)
df['Longitude'] = df['Longitude'].apply(convert_fraction_to_decimal)

# Normalize latitude, longitude, and elevation
df['Latitude'] = normalize_values(df['Latitude'].values)
df['Longitude'] = normalize_values(df['Longitude'].values)
df['Elevation'] = normalize_values(df['Elevation'].values)

fig = px.scatter_3d(df, x='Latitude', y='Longitude', z='Elevation', title='3D Path')

# Define the app layout
app.layout = html.Div([
    dcc.Graph(
        id='scatter-plot',
        figure=fig
    )
])

# Define callback to open external website on point click
@app.callback(
    Output('scatter-plot', 'config'),
    Input('scatter-plot', 'clickData')
)
def open_external_website(click_data):
    if click_data is not None:
        # Extract the URL from the customdata of the clicked point
        url = click_data['points'][0]['customdata']
        # Open the external website in a new tab
        return {'toImageButtonOptions': {'format': 'png', 'filename': 'plot', 'height': 500, 'width': 700},
                'modeBarButtonsToAdd': [
                    {'name': 'Open Website',
                     'icon': 'google.com',
                     'click': f'window.open("{url}", "_blank")'}
                ]}
    else:
        return {}

if __name__ == '__main__':
    app.run_server(debug=True)

