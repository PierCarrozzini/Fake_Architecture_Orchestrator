# config.py

import subprocess
import json


def chiedi_opzione():
    while True:
        scelta = input("Scegli un'opzione (digita 'img', 'xml' o 'compose'): ").lower()
        if scelta in ['img', 'xml', 'compose']:
            return scelta
        else:
            print("Opzione non valida. Riprova.")

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

def run_docker_compose():
    print("Applying Docker compose...")
    subprocess.run("docker compose up -d")
    print("Docker compose applied.")


# PATH DEFINITION

diagram_xml = "drawio_Diagrams/ProvaProprieta.drawio.xml"

docker_config_file = "/Users/orlando/Desktop/FakeArchitectureOrchestrator/project_new/docker_config.json"

#terraform_path = "C://Users//pierc//Documents//Magistrale//2 Anno//1° Semestre//CyberSecurity//Progetto//terraform.exe"
terraform_path = "/Users/orlando/Desktop/FakeArchitectureOrchestrator/project_new/terraform"

image_path = "Images/img2.jpg"
result_img_path = "Images/prediction.jpg"
img_resized_path = "Images/resized.jpg"