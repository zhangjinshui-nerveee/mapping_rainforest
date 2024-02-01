import plotly.graph_objects as go
import numpy as np
from scipy.interpolate import griddata

def read_obj_file(file_path):
    vertices = []

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertex = list(map(float, line.split()[1:]))
                vertices.append(vertex)

    return np.array(vertices)

def plot_obj_map(vertices):
    x = vertices[:, 0]  # Longitude
    y = vertices[:, 1]  # Elevation
    z = vertices[:, 2]  # Altitude

    # Create a grid for surface plot
    xi = np.linspace(min(x), max(x), 100)
    yi = np.linspace(min(y), max(y), 100)
    xi, yi = np.meshgrid(xi, yi)
    zi = griddata((x, y), z, (xi, yi), method='linear')

    fig = go.Figure(data=[go.Surface(z=zi, x=xi, y=yi, colorscale='Viridis')])

    fig.update_layout(scene=dict(
        xaxis_title='Longitude',
        yaxis_title='Elevation',
        zaxis_title='Altitude'
    ))

    fig.show()

if __name__ == "__main__":
    obj_file_path = "your_model.obj"
    obj_vertices = read_obj_file(obj_file_path)
    plot_obj_map(obj_vertices)

