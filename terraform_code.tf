
resource "docker_container" "bVUwOe1Q3J5sBHsqbzTg-1_container" {
  image = "nginx:latest"
  name  = "bVUwOe1Q3J5sBHsqbzTg-1_container"
  volumes = ["./my_web_page:/usr/share/nginx/html"]
}


resource "docker_container" "bVUwOe1Q3J5sBHsqbzTg-2_container" {
  image = "nginx:latest"
  name  = "bVUwOe1Q3J5sBHsqbzTg-2_container"
  volumes = ["./my_web_page:/usr/share/nginx/html"]
}


resource "docker_container" "pdmmIQ8_Or4k_K_Mo9M1-2_container" {
  image = "postgres:latest"
  name  = "pdmmIQ8_Or4k_K_Mo9M1-2_container"
  environment = { "POSTGRES_PASSWORD" = "your_password" }
}

