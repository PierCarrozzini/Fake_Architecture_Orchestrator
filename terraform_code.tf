
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


resource "docker_container" "web_server_2_container" {
  image = "nginx:latest"
  name  = "web_server_2_container"
  volumes {
    host_path      = "C://Users//pierc//PycharmProjects//FakeArchitectureOrchestrator//my_web_page"
    container_path = "/usr/share/nginx/html"
  }
  ports {
    internal = 80
    external = 8081
  }
}


resource "docker_container" "database_4_container" {
  image = "mysql:latest"
  name  = "database_4_container"
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


resource "docker_container" "message_queque_5_container" {
  image = "rabbitmq:latest"
  name  = "message_queque_5_container"
  ports {
    internal = 5672
    external =  5672
  }
}


resource "docker_container" "cache_6_container" {
  image = "redis:latest"
  name  = "cache_6_container"
  ports {
    internal = 6379
    external =  6379
  }
}


resource "docker_container" "cms_7_container" {
  image = "wordpress:latest"
  name  = "cms_7_container"
  volumes {
    container_path = "/var/www/html"
}
  restart = "always"
  env = [ "WORDPRESS_DB_NAME= wordpress","WORDPRESS_DB_PASSWORD= wordpress","WORDPRESS_DB_USER= wordpress","WORDPRESS_DB_HOST= db"]
  ports {
    internal = 80
    external =  8080
  }
}

