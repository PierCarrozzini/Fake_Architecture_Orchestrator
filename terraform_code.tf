
resource "docker_container" "web_server_1_container" {
  image = "nginx:latest"
  name  = "web_server_1_container"
  volumes {
    host_path      = "/Users/orlando/Desktop/FakeArchitectureOrchestrator/project_new/my_web_page"
    container_path = "/usr/share/nginx/html"
  }
  ports {
    internal = 80
    external = 8080
  }
}

