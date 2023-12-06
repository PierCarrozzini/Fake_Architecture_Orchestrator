import json
import subprocess
import terraform_plan_generator
import utils
import xml_Parser
from PIL import Image
from matplotlib import pyplot as plt  # importate anche le librerie contourpy cycler fonttools kiwiresolver numpy


# packaging pyparsing python-dateutil six matplotlib


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


if __name__ == "__main__":
    diagram_xml = utils.diagram_xml
    docker_config_file = utils.docker_config_file
    terraform_path = utils.terraform_path
    image_path = utils.image_path

    # Chiedo all'utente di selezionare un'opzione
    opzione_scelta = chiedi_opzione()

    # Proseguo a seconda dell'opzione selezionata
    if opzione_scelta == 'img':
        print("Hai scelto l'opzione 'img'. Prosegui con il codice relativo a 'img'.")
        print("---IMPLEMENTARE CODICE---")

    elif opzione_scelta == 'compose':
        print("Hai scelto l'opzione 'compose'. Prosegui con il codice relativo a 'compose'.")
        run_docker_compose()

    elif opzione_scelta == 'xml':
        print("Hai scelto l'opzione 'xml'. Proseguo con il codice relativo a 'xml'.")

        print("=== Starting Detection ===")

        image = Image.open(image_path)
        plt.imshow(image)
        plt.axis('off')
        plt.show(block=False)

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
        run_terraform_init(terraform_path)

        # Next step: Apply Terraform Plan
        run_terraform_apply(terraform_path)

        plt.waitforbuttonpress()

        print("\n=== Infrastructure Generation Complete ===")
