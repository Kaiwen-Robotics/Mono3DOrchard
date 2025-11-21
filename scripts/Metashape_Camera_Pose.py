import xml.etree.ElementTree as ET
import os
import numpy as np

# Path to your cameras.xml file
xml_path = '../Task1_withRef/cameras.xml'
output_dir = '../Task1_withRef/CameraPose/poses_output'  # directory to save output text files
os.makedirs(output_dir, exist_ok=True)

# Parse the XML
tree = ET.parse(xml_path)
root = tree.getroot()

# Namespace support if needed (not used in this structure)
# namespace = {'ns': 'your-namespace'}

# Find all camera entries
for camera in root.findall('.//camera'):
    label = camera.get('label')  # e.g., 'frame_0000'
    transform_text = camera.find('transform').text.strip()
    transform_values = list(map(float, transform_text.split()))
    
    # Convert flat list to 4x4 matrix
    matrix = np.array(transform_values).reshape(4, 4)

    # Save to text file
    output_path = os.path.join(output_dir, f'{label}.txt')
    np.savetxt(output_path, matrix, fmt='%.18e')

print(f"Camera poses extracted to: {output_dir}")
