terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.0.2"
    }
    mysql = {
      source = "petoju/mysql"
      version = "3.0.43"
    }
  }
}
provider "docker" {
  host = "npipe:////./pipe/docker_engine"
}
#provider "mysql" {
  # Configuration options
  #endpoint = "localhost"
  #username = ""
  #password = "vvvffss"
#}

resource "docker_image" "test" {
  count = var.create_test_image ? 1 : 0
  name = "test"
  keep_locally = true
}

variable "create_test_image" {
  description = "Whether to create the test image"
  default     = false
}

#resource "docker_container" "example" {
  #name  = "example-container"
  #image = "busybox:latest"
  #command = ["tail", "-f", "/dev/null"]
#}