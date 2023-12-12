import json
import subprocess
import terraform_plan_generator
import utils
import xml_Parser
from PIL import Image
from matplotlib import pyplot as plt  # importate anche le librerie contourpy cycler fonttools kiwiresolver numpy


# packaging pyparsing python-dateutil six matplotlib



if __name__ == "__main__":
    diagram_xml = utils.diagram_xml
    docker_config_file = utils.docker_config_file
    terraform_path = utils.terraform_path
    image_path = utils.image_path

    # Chiedo all'utente di selezionare un'opzione
    opzione_scelta = utils.chiedi_opzione()

    # Proseguo a seconda dell'opzione selezionata
    if opzione_scelta == 'img':
        print("Hai scelto l'opzione 'img'. Prosegui con il codice relativo a 'img'.")
        print("---IMPLEMENTARE CODICE---")

    elif opzione_scelta == 'compose':
        print("Hai scelto l'opzione 'compose'. Prosegui con il codice relativo a 'compose'.")
        utils.run_docker_compose()

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
        docker_config = utils.load_docker_config(docker_config_file)

        print("\n=== Starting Infrastructure Generation ===\n")
        # Generate the terraform plan using detected components and current docker configuration
        terraform_code = terraform_plan_generator.generate_terraform_plan(components, docker_config)

        # Write the generated plan to a .tf file
        utils.write_terraform_code_to_file(terraform_code)

        # Next step: Initialize Terraform
        utils.run_terraform_init(terraform_path)

        # Next step: Apply Terraform Plan
        utils.run_terraform_apply(terraform_path)

        plt.waitforbuttonpress()

        print("\n=== Infrastructure Generation Complete ===")
