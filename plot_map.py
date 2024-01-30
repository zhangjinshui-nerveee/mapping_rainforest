import laspy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_las_point_cloud(las_filename):
    # Open the LAS file
    las_file = laspy.file.File(las_filename, mode="r")

    # Extract X, Y, and Z coordinates from the LAS file
    x_coords = las_file.X
    y_coords = las_file.Y
    z_coords = las_file.Z

    # Create 3D plot
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the point cloud
    ax.scatter(x_coords, y_coords, z_coords, c=z_coords, cmap='viridis', s=0.1)

    # Set axis labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Add colorbar
    cbar = plt.colorbar(ax.scatter(x_coords, y_coords, z_coords, c=z_coords, cmap='viridis', s=0.1), ax=ax)
    cbar.set_label('Elevation (Z)')

    plt.show()

if __name__ == "__main__":
    las_filename = "your_point_cloud.las"  # Replace with the actual LAS file path
    plot_las_point_cloud(las_filename)

