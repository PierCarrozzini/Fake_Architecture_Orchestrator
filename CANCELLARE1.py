import json
import subprocess
import terraform_plan_generator
import xml_Parser


def load_docker_config(config_file):
    print("Loading Docker configuration...")
    with open(config_file, 'r') as f:
        docker_configuration = json.load(f)
    print("...Docker configuration loaded successfully")
    return docker_configuration


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

    diagram_xml = "drawio_Diagrams/ProvaProprieta.drawio.xml"
    docker_config_file = "docker_config.json"
    terraform_path = ("C://Users//pierc//Documents//Magistrale//2 Anno//1° "
                      "Semestre//CyberSecurity//Progetto//terraform.exe")

    print("=== Starting Detection ===")

    # Reading the diagram components from the xml file
    components = xml_Parser.parse_drawio_xml(diagram_xml)

    # Get the configuration file for docker
    docker_config = load_docker_config(docker_config_file)

    print("\n=== Starting Infrastructure Generation ===\n")
    # Generate the terraform plan using detected components and current docker configuration
    terraform_code = terraform_plan_generator.generate_terraform_plan(components, docker_config)

    # Write the generated plan to a .tf file
    write_terraform_code_to_file(terraform_code)

    # Next step: Initialize Terraform
    #run_terraform_init(terraform_path)

    # Next step: Apply Terraform Plan
    #run_terraform_apply(terraform_path)

    print("\n=== Infrastructure Generation Complete ===")
