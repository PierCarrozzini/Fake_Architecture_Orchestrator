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


def generate_terraform_plan(components, docker_config):
    print("Generating Terraform plan...")

    terraform_code = ""
    external_port_web_server = 8079

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

            # Particular configurations based on component type
            if component_type == 'web_server':
                external_port_web_server += 1
                volume_path = docker_config[component_type].get('volume', '')
                terraform_code += (f'  volumes {{\n    host_path      = "{volume_path}"\n    container_path = '
                                   f'"/usr/share/nginx/html"\n  }}\n')
                terraform_code += (f'  ports {{\n    internal = 80\n    external = '
                                   f'{external_port_web_server}\n  }}\n')
                # terraform_code += '}\n\n'

            elif component_type == 'database':

                # MySQL database use case

                db_name = docker_config[component_type].get('name', 'my_database')

                db_user = docker_config[component_type].get('user', 'root')

                db_password = docker_config[component_type].get('password', 'password123')

                database_port = docker_config[component_type].get('port', 3306)  # Sostituire con porta effettiva del db

                terraform_code += (f'  env = [ "MYSQL_DATABASE= {db_name}","MYSQL_ROOT_PASSWORD= {db_password}",'
                                   f'"MYSQL_USER= {db_user}","MYSQL_PASSWORD= {db_password}"]\n')
                terraform_code += (f'  ports {{\n    internal = {database_port}\n    external = '
                                   f' {database_port}\n  }}\n')

            elif component_type == 'cache':

                # Redis cache use case

                cache_port = docker_config[component_type].get('port', '6379')

                terraform_code += (f'  ports {{\n    internal = {cache_port}\n    external = '

                                   f' {cache_port}\n  }}\n')

            elif component_type == 'message_queue':
                # RabbitMQ message queue use case
                mq_port = docker_config[component_type].get('port', '5672')
                terraform_code += (f'  ports {{\n    internal = {mq_port}\n    external = '
                                   f' {mq_port}\n  }}\n')

            elif component_type == 'cms':
                # WordPress use case CMS (Content Management System)
                wp_port = docker_config[component_type].get('port', '8080')
                terraform_code += (f'  ports {{\n    internal = {wp_port}\n    external = '
                                   f' {wp_port}\n  }}\n')
# ################## DA QUI IN POI TUTTO DA TESTARE ######################################
            elif component_type == 'proxy':
                # HAProxy use case
                proxy_port = docker_config[component_type].get('port', '8080')
                terraform_code += (f'  ports {{\n    internal = {proxy_port}\n    external = '
                                   f' {proxy_port}\n  }}\n')

            elif component_type == 'monitoring':
                # Prometheus & Grafana (Monitoraggio e Registrazione)
                prometheus_port = docker_config[component_type].get('prometheus_port', '9090')
                grafana_port = docker_config[component_type].get('grafana_port', '3000')
                terraform_code += (f'  ports {{\n    internal = {prometheus_port}\n    external = '
                                   f' {prometheus_port}\n  }}\n')
                terraform_code += (f'  ports {{\n    internal = {grafana_port}\n    external = '
                                   f' {grafana_port}\n  }}\n')

            elif component_type == 'ci_cd':
                # Jenkins use case (Continuous Integration / Continuous Deployment)
                jenkins_port = docker_config[component_type].get('port', '8080')
                terraform_code += (f'  ports {{\n    internal = {jenkins_port}\n    external = '
                                   f' {jenkins_port}\n  }}\n')

            elif component_type == 'e_commerce':
                # Magento use case
                magento_port = docker_config[component_type].get('port', '8080')
                terraform_code += (f'  ports {{\n    internal = {magento_port}\n    external = '
                                   f' {magento_port}\n  }}\n')

            elif component_type == 'machine_learning':
                # Jupyter Notebook use case
                jupyter_port = docker_config[component_type].get('port', '8888')
                terraform_code += (f'  ports {{\n    internal = {jupyter_port}\n    external = '
                                   f' {jupyter_port}\n  }}\n')

            elif component_type == 'version_control':
                # GitLab use case
                gitlab_port = docker_config[component_type].get('port', '80')
                terraform_code += (f'  ports {{\n    internal = {gitlab_port}\n    external = '
                                   f' {gitlab_port}\n  }}\n')

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
    terraform_path = ("C://Users//pierc//Documents//Magistrale//2 Anno//1° "
                      "Semestre//CyberSecurity//Progetto//terraform.exe")

    print("=== Starting Infrastructure Generation ===")

    components = parse_drawio_xml(diagram_xml)
    docker_config = load_docker_config(docker_config_file)

    terraform_code = generate_terraform_plan(components, docker_config)
    write_terraform_code_to_file(terraform_code)

    # Step 1: Initialize Terraform
    run_terraform_init(terraform_path)

    # Step 2: Apply Terraform Plan
    run_terraform_apply(terraform_path)

    print("=== Infrastructure Generation Complete ===")
