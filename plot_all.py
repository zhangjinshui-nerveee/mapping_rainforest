import pandas as pd
import plotly.graph_objects as go
import numpy as np
from scipy.interpolate import griddata
from fractions import Fraction

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

    # Add custom interaction for the 3D path (click to open a webpage)
    path_trace.hoverinfo = 'text'
    path_trace.text = ['Click to open webpage'] * len(latitude)
    path_trace.customdata = ['https://www.google.com'] * len(latitude)  # Replace with your desired webpage URL

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

    # Add custom interaction for the surface plot (click to open a webpage)
    surface_trace.hoverinfo = 'text'
    surface_trace.text = ['Click to open webpage'] * len(xi.flatten())
    surface_trace.customdata = ['https://www.google.com'] * len(xi.flatten())  # Replace with your desired webpage URL

    # Create a Plotly Figure
    fig = go.Figure(data=[path_trace, surface_trace])

    # Update layout
    fig.update_layout(scene=dict(
        xaxis_title='Normalized Latitude',
        yaxis_title='Normalized Longitude',
        zaxis_title='Normalized Elevation'
    ))

    # Show the combined plot
    fig.show()

if __name__ == "__main__":
    obj_file_path = 'your_model.obj'
    csv_filename = "path_data.csv"  # Replace with the actual CSV file path
    plot_combined(obj_file_path, csv_filename)

