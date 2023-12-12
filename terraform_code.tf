
resource "docker_container" "firewall_0_container" {
  image = "wallarm/api-firewall:latest"
  name  = "firewall_0_container"
  ports {
    internal = 8088
    external =  8088
  }
  restart = "on-failure"
  env = [ "APIFW_REQUEST_VALIDATION= LOG_ONLY", "APIFW_RESPONSE_VALIDATION= LOG_ONLY", "APIFW_API_SPECS= /api-firewall/resources/swagger.json"]
}


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


resource "docker_container" "database_2_container" {
  image = "mysql:latest"
  name  = "database_2_container"
  volumes {
    container_path = "/var/lib/mysql"
}
  restart = "always"
  env = [ "MYSQL_DATABASE= my_database","MYSQL_ROOT_PASSWORD= password123","MYSQL_USER= my_user","MYSQL_PASSWORD= password123"]
  ports {
    internal = 3306
    external =  3306
  }
}


resource "docker_container" "firewall_3_container" {
  image = "wallarm/api-firewall:latest"
  name  = "firewall_3_container"
  ports {
    internal = 8088
    external =  8088
  }
  restart = "on-failure"
  env = [ "APIFW_REQUEST_VALIDATION= LOG_ONLY", "APIFW_RESPONSE_VALIDATION= LOG_ONLY", "APIFW_API_SPECS= /api-firewall/resources/swagger.json"]
}


resource "docker_container" "web_server_4_container" {
  image = "nginx:latest"
  name  = "web_server_4_container"
  volumes {
    host_path      = "/Users/orlando/Desktop/FakeArchitectureOrchestrator/project_new/my_web_page"
    container_path = "/usr/share/nginx/html"
  }
  ports {
    internal = 80
    external = 8081
  }
}

