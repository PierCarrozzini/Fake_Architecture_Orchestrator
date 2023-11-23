import xml.etree.ElementTree as ET
import json
import subprocess


def parse_drawio_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    components = []
    component_counter = 1
    recognized_values = ['web_server', 'database', 'firewall']
    value_counts = {}
    other_value_count = 0

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

        # Aggiunta della logica di conteggio
        value = component_info['value']
        if value in recognized_values:
            if value in value_counts:
                value_counts[value] += 1
                print(f"Found {value} component in the diagram, number = {value_counts[value]}.")
            else:
                value_counts[value] = 1
                print(f"Found {value} component in the diagram, number = {value_counts[value]}.")
        else:
            other_value_count += 1
            print(f"Found a not recognized component in the diagram, number = {other_value_count}.")

    print(f"Found {len(components)} components in the diagram.")

    # Creating individual variables for each unique value
    for value, count in value_counts.items():
        if value in recognized_values:
            globals()[value] = count  # Avoid this if possible; use a dictionary instead
            print(f"Number of '{value}' components: {count}")
    print(f"Number of not recognized components: {other_value_count}")

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
    external_port = 8079

    for component in components:
        component_type = component['type']
        container_name = f"{component['type']}_{component['number']}_container"

        if component_type in docker_config:
            docker_image = docker_config[component_type].get('image', 'default_docker_image')
            terraform_code += f'''
resource "docker_container" "{container_name}" {{
  image = "{docker_image}"
  name  = "{container_name}"
'''

            # Additional configurations based on component type
            if component_type == 'web_server':
                external_port += 1
                volume_path = docker_config[component_type].get('volume', '')
                terraform_code += (f'  volumes {{\n    host_path      = "{volume_path}"\n    container_path = '
                                   f'"/usr/share/nginx/html"\n  }}\n')
                terraform_code += (f'  ports {{\n    internal = 80\n    external = '
                                   f'{external_port}\n  }}\n')

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


def run_terraform_init(path):
    print("Initializing Terraform...")
    subprocess.run([path, "init"])
    print("Terraform initialized.")


def run_terraform_apply(path):
    print("Applying Terraform plan...")
    subprocess.run([path, "apply", "-auto-approve"])
    print("Terraform plan applied.")


if __name__ == "__main__":
    diagram_xml = "drawio_Diagrams/TestProva.drawio.xml"
    docker_config_file = "docker_config.json"
    terraform_path = "C://Users//pierc//Documents\Magistrale//2 Anno//1° Semestre//CyberSecurity//Progetto//terraform.exe"

    print("=== Starting Infrastructure Generation ===")

    components = parse_drawio_xml(diagram_xml)
    docker_config = load_docker_config(docker_config_file)

    terraform_code = generate_terraform_plan(components, docker_config)
    write_terraform_code_to_file(terraform_code)

    # Step 1: Initialize Terraform
    #run_terraform_init(terraform_path)

    # Step 2: Apply Terraform Plan
    #run_terraform_apply(terraform_path)

    print("=== Infrastructure Generation Complete ===")
