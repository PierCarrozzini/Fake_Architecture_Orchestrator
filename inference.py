from roboflow import Roboflow

import terraform_plan_generator
import cv2
import json
import subprocess
import utils
import random

default_value1 = '80'
default_value2 = 8080


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


height, width = 640, 640
docker_config_file = "/Users/orlando/Desktop/FakeArchitectureOrchestrator/project_new/docker_config.json"
terraform_path = "/Users/orlando/Desktop/FakeArchitectureOrchestrator/project_new/terraform"

# MODEL DATA
rf = Roboflow(api_key="2Lzj7j22xAnU96C9ryIQ")
project = rf.workspace().project("architecture_diagrams")
model = project.version(7).model

image = cv2.imread("/Users/orlando/Desktop/FakeArchitectureOrchestrator/project_new/Images/img.png")
result = "/Users/orlando/Desktop/FakeArchitectureOrchestrator/project_new/Images/prediction.jpg"

image_resized = cv2.resize(image, (height, width))
# image = np.expand_dims(image, axis=0)

image_resized = cv2.imwrite("/Users/orlando/Desktop/test.jpg", image_resized)

image_1 = "/Users/orlando/Desktop/test.jpg"

# infer on a local image
results = model.predict(image, confidence=40, overlap=30).json()
# print(results)

# Supponendo che il dizionario sia assegnato a una variabile chiamata prediction_result
prediction_result = results

# stampa predictions
model.predict(image_1, confidence=50, overlap=30).save(result)

# Inizializza una stringa vuota per contenere i risultati
# result_string = ""
# result_stringa = ""


# array di components
components = []

index = 0

# Itera attraverso le previsioni
# VA MODIFICATO SOLO IL NUMBER CHE DEVE DIPENDERE DAL TYPE

for prediction in prediction_result['predictions']:
    # result_string = prediction['class']
    result_stringa = f"Class: {prediction['class']}, Confidence: {prediction['confidence']:.4f}\n"
    # result_string += f"Bounding Box: (x={prediction['x']}, y={prediction['y']}, width={prediction['width']}, height={prediction['height']})\n\n"
    print(result_stringa)

    component = {}
    component['type'] = prediction['class']
    #component['value'] = prediction['class']
    component['number'] = index
    component['name'] = prediction['confidence']
    #component['name'] = f"{component['type']}_{component['number']}_container"
    """ 
    component['Internal_port'] = str(random.randrange(80, 110))
    component['External_port'] = None
    component['style'] = None
    component['x'] = prediction['x']
    component['y'] = prediction['y']
    component['width'] = prediction['width']
    component['height'] = prediction['height']
    """
    """
    component = {
        "number": index,
        "id": index,
        "type": prediction['class'],
        "name": prediction['confidence'],
        "value": prediction['class'],
        "Internal_port": random.randrange(80, 110) if prediction['class'] is not None else default_value1,
        "External_port": random.randrange(8080, 8090) if prediction['class'] is not None else default_value2,
        "style": prediction['confidence'],
        "x": prediction['x'],
        "y": prediction['y'],
        "width": prediction['width'],
        "height": prediction['height']
    }
    """
    components.append(component)
    index = index + 1


# Get the configuration file for docker
docker_config = load_docker_config(docker_config_file)

# Generate the terraform plan using detected components and current docker configuration
code = terraform_plan_generator.generate_terraform_plan(components, docker_config)

#print(code)

# Write the generated plan to a .tf file
write_terraform_code_to_file(code)

# Next step: Initialize Terraform
run_terraform_init(terraform_path)

# Next step: Apply Terraform Plan
run_terraform_apply(terraform_path)

print("\n=== Infrastructure Generation Complete ===")

# Stampa o utilizza la stringa risultante come desiderato


# visualize your prediction
# model.predict(image_1, confidence=50, overlap=30).save(result)

# infer on an image hosted elsewhere
# print(model.predict("URL_OF_YOUR_IMAGE", hosted=True, confidence=40, overlap=30).json())


# print("=== Starting Detection ===")
