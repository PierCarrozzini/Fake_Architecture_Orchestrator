
resource "docker_container" "web_server_1_container" {
  image = "nginx:latest"
  name  = "web_server_1_container"
  volumes {
    host_path      = "C://Users//pierc//PycharmProjects//FakeArchitectureOrchestrator//my_web_page"
    container_path = "/usr/share/nginx/html"
  }
  ports {
    internal = 80
    external = 8080
  }
}


resource "docker_container" "grafana_6_container" {
  image = "grafana/grafana:latest"
  name  = "grafana_6_container"
  ports {
    internal = 3000
    external =  3000
  }
}


resource "docker_container" "prometheus_7_container" {
  image = "ubuntu/prometheus:2.48.0-22.04_stable"
  name  = "prometheus_7_container"
  ports {
    internal = 9090
    external =  9090
  }
}

