# config.py

import subprocess
import json

# PATH DEFINITION

diagram_xml = "drawio_Diagrams/final.drawio.xml"
diagram_img = "Images/final.jpg"

#docker_config_file = "/Users/orlando/Desktop/FakeArchitectureOrchestrator/project_new/docker_config.json"
docker_config_file = "docker_config.json"

terraform_path = "C://Users//pierc//Documents//Magistrale//2 Anno//1° Semestre//CyberSecurity//Progetto//terraform.exe"
#terraform_path = "/Users/orlando/Desktop/FakeArchitectureOrchestrator/project_new/terraform"

image_path = "Images/test.jpg"
result_img_path = "Images/prediction.jpg"
img_resized_path = "Images/resized.jpg"


# FUNCTION DEFINITION

def chiedi_img():
    while True:
        scelt = input(" \nFornire il path dell'immagine da analizzare o default per l'immagine predefinita: ").lower()
        if scelt in ['Default', 'default']:
            return image_path
        else:
            print("Hai scelto la seguente immagine:", scelt)
            return scelt


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
