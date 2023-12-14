from roboflow import Roboflow
import terraform_plan_generator
import cv2
import utils

height, width = 640, 640

# MODEL DATA
rf = Roboflow(api_key="2Lzj7j22xAnU96C9ryIQ")
project = rf.workspace().project("architecture_diagrams")
model = project.version(7).model


def img_parser():

    print("----- IMG_PARSER STARTING -----")

    imag = utils.chiedi_img()

    # LOAD IMAGE FOR INFERENCE

    image = cv2.imread(imag)

    # cv2.imshow("IMAGE", image)
    # cv2.waitKey(0)

    # ADJUST IMAGE FOR PREDICTION

    image_resized = cv2.resize(image, (height, width))

    # cv2.imshow("IMAGE_RESIZED", image_resized)
    # cv2.waitKey(0)

    image_resized = cv2.imwrite(utils.img_resized_path, image_resized)

    # PREDICTION

    prediction_result = model.predict(utils.img_resized_path, confidence=40, overlap=30).json()

    model.predict(utils.img_resized_path, confidence=50, overlap=30).save(utils.result_img_path)

    # VARIABILI UTILI

    components = []
    index = 0

    # Itera attraverso le previsioni

    for prediction in prediction_result['predictions']:
        result_stringa = f"Class: {prediction['class']}, Confidence: {prediction['confidence']:.4f}\n"
        print(result_stringa)
        component = {}
        component['type'] = prediction['class']
        component['number'] = index
        component['name'] = prediction['confidence']
        components.append(component)
        index += 1

    # Get the configuration file for docker
    docker_config = utils.load_docker_config(utils.docker_config_file)

    # Generate the terraform plan using detected components and current docker configuration
    code = terraform_plan_generator.generate_terraform_plan(components, docker_config)

    # Write the generated plan to a .tf file
    utils.write_terraform_code_to_file(code)

    # Next step: Initialize Terraform
    utils.run_terraform_init(utils.terraform_path)

    # Next step: Apply Terraform Plan
    utils.run_terraform_apply(utils.terraform_path)

    print("\n=== Infrastructure Generation Complete ===")
