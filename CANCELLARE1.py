import xml.etree.ElementTree as ET
import json
import subprocess


def parse_drawio_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    components = []
    component_counter = 1

    for cell_elem in root.findall('.//mxCell[@vertex="1"]'):
        component_info = {}

        component_info['number'] = component_counter
        component_counter += 1

        # Extract information about each vertex (component)
        component_info['id'] = cell_elem.get('id')
        component_info['name'] = cell_elem.get('id')
        component_info['value'] = cell_elem.get('value')
        component_info['type'] = cell_elem.get('value')
        component_info['style'] = cell_elem.get('style')

        # Extract geometry information
        geometry_elem = cell_elem.find('mxGeometry')
        if geometry_elem is not None:
            component_info['x'] = geometry_elem.get('x')
            component_info['y'] = geometry_elem.get('y')
            component_info['width'] = geometry_elem.get('width')
            component_info['height'] = geometry_elem.get('height')

        components.append(component_info)
        print(f"Component :")
        print(f"Number: {component_info['number']}")
        print(f"ID: {component_info['id']}")
        print(f"Name: {component_info['id']}")
        print(f"Value: {component_info['value']}")
        print(f"Type: {component_info['value']}")
        print(f"Style: {component_info['style']}")
        print(f"Position: ({component_info['x']}, {component_info['y']})")
        print(f"Size: {component_info['width']} x {component_info['height']}")
        print()
    print(f"Found {len(components)} components in the diagram.")

    return components


def load_docker_config(config_file):
    print("Loading Docker configuration...")
    with open(config_file, 'r') as f:
        docker_config = json.load(f)
    return docker_config


# ############## QUI ABBIAMO DIVERSI CASI DI TERRAFORM PLAN CON WEB_SERVER E DATABASE
# ############ PER ORA CI SONO SOLO QUESTI 2 BISOGNA AGGIUNGERE ALTRI CASI (FIREWALL ECC)
# LAVORARE SU generate_infrastructure.py, docker_config.json, terraform_code.tf (autogenerato), my_web_page.
# CAPIRE cosa aggiungere in docker_config (firewall ecc) e TESTARE FUNZIONAMENTO DEI CASI ESISTENTI
def generate_terraform_plan(components, docker_config):
    print("Generating Terraform plan...")

    terraform_code = ""

    for component in components:
        component_type = component['type']
        container_name = f"{component['name']}_container"

        if component_type in docker_config:
            docker_image = docker_config[component_type].get('image', 'default_docker_image')
            terraform_code += f'''
resource "docker_container" "{container_name}" {{
  image = "{docker_image}"
  name  = "{container_name}"
'''

            # Additional configurations based on component type
            if component_type == 'web_server':
                volume_path = docker_config[component_type].get('volume', '')
                terraform_code += f'  volumes = ["{volume_path}:/usr/share/nginx/html"]\n'
            elif component_type == 'database':
                environment_vars = docker_config[component_type].get('environment', {})
                for var_name, var_value in environment_vars.items():
                    terraform_code += f'  environment = {{ "{var_name}" = "{var_value}" }}\n'

            terraform_code += '}\n\n'

    print("Terraform plan generated.")
    return terraform_code


def write_terraform_code_to_file(code, output_file="terraform_code.tf"):
    print(f"Writing Terraform code to {output_file}...")
    with open(output_file, 'w') as f:
        f.write(code)

    print("Terraform code written.")


def run_terraform_init():
    print("Initializing Terraform...")
    subprocess.run(["terraform", "init"])
    print("Terraform initialized.")


def run_terraform_apply():
    print("Applying Terraform plan...")
    subprocess.run(["terraform", "apply", "-auto-approve"])
    print("Terraform plan applied.")


if __name__ == "__main__":
    diagram_xml = "web_server_diagram.xml"
    docker_config_file = "docker_config.json"

    print("=== Starting Infrastructure Generation ===")

    components = parse_drawio_xml(diagram_xml)
    docker_config = load_docker_config(docker_config_file)

    terraform_code = generate_terraform_plan(components, docker_config)
    write_terraform_code_to_file(terraform_code)

    # Step 1: Initialize Terraform
    # run_terraform_init()

    # Step 2: Apply Terraform Plan
    # run_terraform_apply

    print("=== Infrastructure Generation Complete ===")