
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


resource "docker_container" "database_3_container" {
  image = "mysql:latest"
  name  = "database_3_container"
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


resource "docker_container" "firewall_4_container" {
  image = "alpine:latest"
  name  = "firewall_4_container"
  restart = "always"
 command = ["ash", "-c", "apk update && apk add iptables && iptables -A INPUT -p tcp --dport 80 -j ACCEPT && iptables -A INPUT -p udp --dport 53 -j DROP && exec tail -f /dev/null"]
}


resource "docker_container" "message_queque_6_container" {
  image = "rabbitmq:latest"
  name  = "message_queque_6_container"
  ports {
    internal = 5672
    external =  5672
  }
  restart = "always"
  env = [ "RABBITMQ_DEFAULT_VHOST= /", "RABBITMQ_DEFAULT_USER= my_rabbitmq_user", "RABBITMQ_DEFAULT_PASS= my_rabbitmq_password"]
}


resource "docker_container" "proxy_15_container" {
  image = "haproxy:latest"
  name  = "proxy_15_container"
  volumes {
    host_path      = "C:/Users/pierc/Downloads/haproxy.cfg"
    container_path ="/usr/local/etc/haproxy/haproxy.cfg"
    read_only = "true"
}
  ports {
    internal = 80
    external = 80
  }
  env = [ "MAXCONN= 4096","MODE= http","HTTP_CHECK= disable-on-404","STATS_PORT= 1936","STATS_AUTH= username:password","TIMEOUT_CONNECT= 5000","TIMEOUT_CLIENT= 50000","TIMEOUT_SERVER= 50000"]
}


resource "docker_container" "prometheus_17_container" {
  image = "ubuntu/prometheus:2.48.0-22.04_stable"
  name  = "prometheus_17_container"
  ports {
    internal = 9090
    external =  9090
  }
}


resource "docker_container" "grafana_18_container" {
  image = "grafana/grafana:latest"
  name  = "grafana_18_container"
  ports {
    internal = 3000
    external =  3000
  }
}


resource "docker_container" "machine_learning_19_container" {
  image = "jupyter/scipy-notebook:latest"
  name  = "machine_learning_19_container"
  ports {
    internal = 8888
    external =  8888
  }
  env = [ "JUPYTER_ENABLE_LAB= yes"]
 command = ["start-notebook.sh", "--NotebookApp.token=", "--NotebookApp.password="]
}

