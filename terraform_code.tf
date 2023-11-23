
resource "docker_container" "message_queue_4_container" {
  image = "rabbitmq:latest"
  name  = "message_queue_4_container"
  ports {
    internal = 5672
    external =  5672
  }
}


resource "docker_container" "cms_5_container" {
  image = "wordpress:latest"
  name  = "cms_5_container"
  ports {
    internal = 8080
    external =  8080
  }
}

