import pandas as pd
import plotly.graph_objects as go
import numpy as np
from scipy.interpolate import griddata
from fractions import Fraction
import dash
from dash import dcc, html, Input, Output, State
import os

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

def read_obj_file(file_path):
    vertices = []

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertex = list(map(float, line.split()[1:]))
                vertices.append(vertex)

    return np.array(vertices)

def plot_combined(obj_file_path, csv_filename):
    # Read CSV file into a DataFrame
    df = pd.read_csv(csv_filename)

    # Convert latitude and longitude from fractions to decimals
    df['Latitude'] = df['Latitude'].apply(convert_fraction_to_decimal)
    df['Longitude'] = df['Longitude'].apply(convert_fraction_to_decimal)

    # Normalize latitude, longitude, and elevation
    df['Latitude'] = normalize_values(df['Latitude'].values)
    df['Longitude'] = normalize_values(df['Longitude'].values)
    df['Elevation'] = normalize_values(df['Elevation'].values)

    # Sort DataFrame by the "Filename" column
    df = df.sort_values(by='Filename')

    # Extract coordinates and elevation
    latitude = df['Latitude'].values
    longitude = df['Longitude'].values
    elevation = df['Elevation'].values

    # Create a 3D scatter plot for the 3D path
    path_trace = go.Scatter3d(
        x=latitude,
        y=longitude,
        z=elevation,
        mode='markers+lines',
        marker=dict(size=4, color='blue'),
        line=dict(color='blue', width=2),
        name='3D Path'
    )

    # Read OBJ file and create a grid for surface plot
    obj_vertices = read_obj_file(obj_file_path)
    x = obj_vertices[:, 0]  # Longitude
    y = obj_vertices[:, 1]  # Elevation
    z = obj_vertices[:, 2]  # Altitude

    # Normalize longitude, altitude, and elevation for the surface plot
    x = normalize_values(x)
    y = normalize_values(y)
    z = normalize_values(z)

    xi = np.linspace(min(x), max(x), 100)
    yi = np.linspace(min(y), max(y), 100)
    xi, yi = np.meshgrid(xi, yi)
    zi = griddata((x, y), z, (xi, yi), method='linear')

    # Create a 3D surface plot
    surface_trace = go.Surface(z=zi, x=xi, y=yi, colorscale='Viridis', name='Surface Plot')

    # Create a Plotly Figure
    fig = go.Figure(data=[path_trace, surface_trace])

    # Update layout
    fig.update_layout(scene=dict(
        xaxis_title='Normalized Latitude',
        yaxis_title='Normalized Longitude',
        zaxis_title='Normalized Elevation'
    ))

    return fig

obj_file_path = 'your_obj_file.obj'
csv_filename = 'your_csv_file.csv'
naming_list = pd.read_csv(csv_filename)['Filename']
print(naming_list)
fig = plot_combined(obj_file_path, csv_filename)

app.layout = html.Div([
    html.Div([
        dcc.Graph(id='main-graph', figure=fig)
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '10px', 'border-right': '2px solid #ccc'}),
    html.Div([
        html.Img(id='image-display', style={'width': '100%'})
    ], style={'width': '29%', 'display': 'inline-block', 'padding': '10px'})
])

app.layout = html.Div([
    dcc.Store(id='clicked-point'),  # Store for the clicked point index
    html.Div([
        dcc.Graph(id='main-graph', figure=fig)
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '10px', 'border-right': '2px solid #ccc'}),
    html.Div([
        html.Img(id='image-display', style={'width': '100%'})
    ], style={'width': '29%', 'display': 'inline-block', 'padding': '10px'})
])

@app.callback(
    Output('clicked-point', 'data'),
    [Input('main-graph', 'clickData')]
)
def store_clicked_point(clickData):
    if clickData is not None and 'points' in clickData and len(clickData['points']) > 0 and 'pointNumber' in clickData['points'][0]:
        return clickData['points'][0]['pointNumber']
    return None

@app.callback(
    Output('main-graph', 'figure'),
    [Input('clicked-point', 'data')],
    [State('main-graph', 'figure')]
)
def update_point_color(clicked_point, fig):
    if clicked_point is not None:
        if 'marker' in fig['data'][0] and 'color' in fig['data'][0]['marker']:
            fig['data'][0]['marker']['color'] = ['red' if i == clicked_point else 'blue' for i in range(len(naming_list))]
    return fig

@app.callback(
    Output('image-display', 'src'),
    [Input('clicked-point', 'data')]
)
def update_image(clicked_point):
    local_path = '/assets/'
    if clicked_point is not None:
        image_filename = naming_list[clicked_point]
        image_path = local_path + image_filename
        return image_path
    return ''

if __name__ == '__main__':
    app.run_server(debug=True)

