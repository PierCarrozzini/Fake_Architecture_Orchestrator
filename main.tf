#https://www.cyberithub.com/step-by-step-guide-to-setup-terraform-in-pycharm-on-windows-10/
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.0.2"
    }
  }
}
provider "docker" {
  host = "npipe:////./pipe/docker_engine"
}

resource "docker_image" "test" {
  name = "test"
  keep_locally = true
}

resource "docker_container" "example" {
  name  = "example-container"
  image = "busybox:latest"
  command = ["tail", "-f", "/dev/null"]
}