import terraform_plan_generator
import utils
import xml_Parser
import img_parser
from PIL import Image
from matplotlib import pyplot as plt

if __name__ == "__main__":

    # Chiedo all'utente di selezionare un'opzione
    opzione_scelta = utils.chiedi_opzione()

    # Proseguo a seconda dell'opzione selezionata
    if opzione_scelta == 'img':
        print("Hai scelto l'opzione 'img_parser'. Prosegui con il codice relativo a 'img'.")
        img_parser.img_parser()

    elif opzione_scelta == 'compose':
        print("Hai scelto l'opzione 'compose'. Prosegui con il codice relativo a 'compose'.")
        utils.run_docker_compose()

    elif opzione_scelta == 'xml':
        print("Hai scelto l'opzione 'xml'. Proseguo con il codice relativo a 'xml'.")

        print("=== Starting Detection ===")

        image = Image.open(utils.image_path)
        plt.imshow(image)
        plt.axis('off')
        plt.show(block=False)

        # Reading the diagram components from the xml file
        components = xml_Parser.parse_drawio_xml(utils.diagram_xml)
        print(components)

        # Get the configuration file for docker
        docker_config = utils.load_docker_config(utils.docker_config_file)

        print("\n=== Starting Infrastructure Generation ===\n")
        # Generate the terraform plan using detected components and current docker configuration
        terraform_code = terraform_plan_generator.generate_terraform_plan(components, docker_config)

        # Write the generated plan to a .tf file
        utils.write_terraform_code_to_file(terraform_code)

        # Next step: Initialize Terraform
        utils.run_terraform_init(utils.terraform_path)

        # Next step: Apply Terraform Plan
        utils.run_terraform_apply(utils.terraform_path)

        plt.waitforbuttonpress()

        print("\n=== Infrastructure Generation Complete ===")
