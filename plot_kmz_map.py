import zipfile
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def extract_kmz(kmz_file_path):
    with zipfile.ZipFile(kmz_file_path, 'r') as zip_ref:
        # Extract the KML file from the KMZ archive
        zip_ref.extractall("temp_folder")

def parse_kml(kml_file_path):
    tree = ET.parse(kml_file_path)
    root = tree.getroot()

    # Namespace for KML
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}

    # Extract coordinates
    coordinates = root.findall('.//kml:coordinates', namespaces=ns)
    print(coordinates)

    # Extract altitude, longitude, and elevation from coordinates
    altitude = []
    longitude = []
    elevation = []

    for coord in coordinates:
        coords = coord.text.strip().split(',')
        longitude.append(float(coords[0]))
        elevation.append(float(coords[1]))
        altitude.append(float(coords[2]))

    return altitude, longitude, elevation

def plot_3d_map(altitude, longitude, elevation):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(longitude, elevation, altitude, c='b', marker='o')

    ax.set_xlabel('Longitude')
    ax.set_ylabel('Elevation')
    ax.set_zlabel('Altitude')

    plt.show()

def main():
    kmz_file_path= 'your_kmz_file.kmz'

    # Extract KMZ file
    extract_kmz(kmz_file_path)

    # Assuming the extracted KML file is named 'doc.kml'
    kml_file_path = 'temp_folder/doc.kml'

    # Parse KML file
    altitude, longitude, elevation = parse_kml(kml_file_path)
    print(altitude)

    # Plot 3D map
    plot_3d_map(altitude, longitude, elevation)

if __name__ == "__main__":
    main()

