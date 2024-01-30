import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from fractions import Fraction

def convert_fraction_to_decimal(fraction_string):
    try:
        fraction = Fraction(fraction_string)
        return float(fraction)
    except ValueError:
        return None

def plot_3d_path(csv_filename):
    # Read CSV file into a DataFrame
    df = pd.read_csv(csv_filename)

    # Convert latitude and longitude from fractions to decimals
    df['Latitude'] = df['Latitude'].apply(convert_fraction_to_decimal)
    df['Longitude'] = df['Longitude'].apply(convert_fraction_to_decimal)

    # Sort DataFrame by the "Filename" column
    df = df.sort_values(by='Filename')

    # Extract coordinates and elevation
    latitude = df['Latitude'].values
    longitude = df['Longitude'].values
    elevation = df['Elevation'].values

    # Create a 3D plot
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the 3D path
    ax.plot(latitude, longitude, elevation, marker='o', linestyle='-', color='b')

    # Set axis labels
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_zlabel('Elevation')

    # Display the plot
    plt.show()

if __name__ == "__main__":
    csv_filename = "path_data.csv"  # Replace with the actual CSV file path
    plot_3d_path(csv_filename)

