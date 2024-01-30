import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import numpy as np

def read_obj_file(obj_filename):
    vertices = []
    faces = []

    with open(obj_filename, 'r') as obj_file:
        for line in obj_file:
            if line.startswith('v '):
                vertex = list(map(float, line.strip().split()[1:]))
                vertices.append(vertex)
            elif line.startswith('f '):
                face = [int(index.split('/')[0]) for index in line.strip().split()[1:]]
                faces.append(face)

    return np.array(vertices), faces

def plot_3d_model(obj_filename):
    vertices, faces = read_obj_file(obj_filename)

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot vertices
    ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], c='b', marker='o')

    # Plot faces
    poly3d = Poly3DCollection([vertices[face] for face in faces], alpha=0.5, edgecolor='k')
    ax.add_collection3d(poly3d)

    # Set axis labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()

if __name__ == "__main__":
    obj_filename = "your_model.obj"  # Replace with the actual .obj file path
    plot_3d_model(obj_filename)

