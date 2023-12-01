import xml.etree.ElementTree as ET
import json


# 3
def detect_components(root, config):
    components = {}

    for element in root.iter():
        if element.tag == 'object':
            component_type = element.get('label')
            component_id = element.get('id')

            if component_type in config['components']:
                docker_image = config['components'][component_type]['docker_image']

                components[component_id] = {
                    'type': component_type,
                    'docker_image': docker_image
                }

        elif element.tag == 'mxCell':
            component_type = element.get('value')
            component_id = element.get('id')

            if component_type in config['components']:
                docker_image = config['components'][component_type]['docker_image']

                components[component_id] = {
                    'type': component_type,
                    'docker_image': docker_image
                }

    return components


# #3

# 4
def generate_terraform_plan(components):
    terraform_plan = ""

    for component_id, details in components.items():
        # Add logic to generate Terraform resources based on component details
        terraform_plan += f"""
resource "docker_container" "{details['type']}_{component_id}" {{
  image = "{details['docker_image']}"
  # Add more resource attributes as needed
}}

        """

    return terraform_plan


# #4

def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Print the root tag
    print(f"Root Tag: {root.tag}")

    # Load configuration    (2)
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

        # Detect components     (3)
        detected_components = detect_components(root, config)
        print("Detected Components:")
        for component_id, details in detected_components.items():
            print(f"Component ID: {component_id}, Type: {details['type']}, Docker Image: {details['docker_image']}")

    # Access Docker image for a component type    (2)
    web_server_image = config['components']['web_server']['docker_image']
    print(f"Web Server Docker Image: {web_server_image}")

    # Iterate through elements
    for element in root.iter():
        print(f"Element Tag: {element.tag}, Element Text: {element.text}, Element Value: {element.get(key='value')}")

    # Generate Terraform plan     (4)
    terraform_plan = generate_terraform_plan(detected_components)
    print("\nTerraform Plan:")
    print(terraform_plan)


if __name__ == "__main__":
    xml_file_path = "drawio_Diagrams/ProvaProprieta.drawio.xml"
    parse_xml(xml_file_path)
