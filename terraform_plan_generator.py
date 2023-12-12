def generate_terraform_plan(components, docker_config):
    print("Generating Terraform plan...")

    terraform_code = ""
    external_port_web_server = 8079

    for component in components:
        component_type = component['type']
        container_name = f"{component['type']}_{component['number']}_container"
        #internal_port = component['Internal_port']

        if component_type in docker_config:
            docker_image = docker_config[component_type].get('image', 'default_docker_image')
            terraform_code += f'''
resource "docker_container" "{container_name}" {{
  image = "{docker_image}"
  name  = "{container_name}"
'''

            # Particular configurations based on component type
            if component_type == 'web_server':
                external_port_web_server += 1
                volume_path = docker_config[component_type].get('volume', '')
                terraform_code += (f'  volumes {{\n    host_path      = "{volume_path}"\n    container_path = '
                                   f'"/usr/share/nginx/html"\n  }}\n')
                terraform_code += (f'  ports {{\n    internal = 80\n    external = '
                                   f'{external_port_web_server}\n  }}\n')
                # terraform_code += '}\n\n'

            elif component_type == 'database':

                # MySQL database use case

                db_name = docker_config[component_type].get('name', 'database')

                db_user = docker_config[component_type].get('user', 'user')

                db_password = docker_config[component_type].get('password', 'password123')

                database_port = docker_config[component_type].get('port', 3306)  # Sostituire con porta effettiva del db

                volume_path = docker_config[component_type].get('db_data', '')

                restart = docker_config[component_type].get('restart', '')

                terraform_code += f'  volumes {{\n    container_path = "{volume_path}"\n}}\n'
                terraform_code += f'  restart = "{restart}"\n'
                terraform_code += (f'  env = [ "MYSQL_DATABASE= {db_name}","MYSQL_ROOT_PASSWORD= {db_password}",'
                                   f'"MYSQL_USER= {db_user}","MYSQL_PASSWORD= {db_password}"]\n')
                terraform_code += (f'  ports {{\n    internal = {database_port}\n    external = '
                                   f' {database_port}\n  }}\n')

            elif component_type == 'firewall':

                # API-Firewall use case

                firewall_port = docker_config[component_type].get('port', '8088')
                restart = docker_config[component_type].get('restart', '')
                HOST_PATH_TO_SPEC = docker_config[component_type].get('HOST_PATH_TO_SPEC', 'LOG_ONLY')
                CONTAINER_PATH_TO_SPEC = docker_config[component_type].get('CONTAINER_PATH_TO_SPEC', 'LOG_ONLY')
                APIFW_REQUEST_VALIDATION = docker_config[component_type].get('APIFW_REQUEST_VALIDATION', 'LOG_ONLY')
                APIFW_RESPONSE_VALIDATION = docker_config[component_type].get('APIFW_RESPONSE_VALIDATION', 'LOG_ONLY')
                APIFW_API_SPECS = docker_config[component_type].get('APIFW_API_SPECS', '')
                APIFW_URL = docker_config[component_type].get('APIFW_URL', '')
                APIFW_SERVER_URL = docker_config[component_type].get('APIFW_SERVER_URL', '')

                # terraform_code += f'  volumes {{\n   <{HOST_PATH_TO_SPEC}> = "<{CONTAINER_PATH_TO_SPEC}>"\n}}\n'
                terraform_code += (f'  ports {{\n    internal = {firewall_port}\n    external = '
                                   f' {firewall_port}\n  }}\n')
                terraform_code += f'  restart = "{restart}"\n'
                terraform_code += (f'  env = [ "APIFW_REQUEST_VALIDATION= {APIFW_REQUEST_VALIDATION}", '
                                   f'"APIFW_RESPONSE_VALIDATION= {APIFW_RESPONSE_VALIDATION}", "APIFW_API_SPECS= '
                                   f'{APIFW_API_SPECS}"]\n')
            # "APIFW_URL= {APIFW_URL}", "APIFW_SERVER_URL= {APIFW_SERVER_URL}"

            elif component_type == 'firewall-alpine':

                # Alpine-Firewall use case

                command = docker_config[component_type].get('command', '')
                restart = docker_config[component_type].get('restart', '')

                terraform_code += f'  restart = "{restart}"\n'
                terraform_code += (f' command = ["ash", "-c", "apk update && apk add iptables && iptables -A INPUT -p '
                                   f'tcp --dport 80 -j ACCEPT && iptables -A INPUT -p udp --dport 53 -j DROP && exec '
                                   f'tail -f /dev/null"]\n')

            elif component_type == 'cache':

                # Redis cache use case

                cache_port = docker_config[component_type].get('port', '6379')
                command = docker_config[component_type].get('command', '')
                restart = docker_config[component_type].get('restart', '')
                REDIS_PASSWORD = docker_config[component_type].get('REDIS_PASSWORD', 'password123')
                REDIS_MAXMEMORY = docker_config[component_type].get('REDIS_MAXMEMORY', '50mb')
                REDIS_APPENDONLY = docker_config[component_type].get('REDIS_APPENDONLY', 'yes')

                terraform_code += (f'  ports {{\n    internal = {cache_port}\n    external = '
                                   f' {cache_port}\n  }}\n')
                terraform_code += f'  restart = "{restart}"\n'
                # terraform_code += f' command = "{command}"\n'
                terraform_code += (
                    f'  env = [ "REDIS_PASSWORD= {REDIS_PASSWORD}", "REDIS_MAXMEMORY= {REDIS_MAXMEMORY}",'
                    f'"REDIS_APPENDONLY= {REDIS_APPENDONLY}"]\n')

            elif component_type == 'message_queque':
                # RabbitMQ message queue use case

                mq_port = docker_config[component_type].get('port', '5672')
                restart = docker_config[component_type].get('restart', '')
                RABBITMQ_DEFAULT_VHOST = docker_config[component_type].get('RABBITMQ_DEFAULT_VHOST', '/')
                RABBITMQ_DEFAULT_USER = docker_config[component_type].get('RABBITMQ_DEFAULT_USER', 'myuser')
                RABBITMQ_DEFAULT_PASS = docker_config[component_type].get('RABBITMQ_DEFAULT_PASS', 'mypass')

                terraform_code += (f'  ports {{\n    internal = {mq_port}\n    external = '
                                   f' {mq_port}\n  }}\n')
                terraform_code += f'  restart = "{restart}"\n'
                # terraform_code += f' command = "{command}"\n'
                terraform_code += (f'  env = [ "RABBITMQ_DEFAULT_VHOST= {RABBITMQ_DEFAULT_VHOST}",'
                                   f' "RABBITMQ_DEFAULT_USER= {RABBITMQ_DEFAULT_USER}",'
                                   f' "RABBITMQ_DEFAULT_PASS= {RABBITMQ_DEFAULT_PASS}"]\n')

            elif component_type == 'cms':
                # WordPress use case CMS (Content Management System)

                db_name = docker_config[component_type].get('WORDPRESS_DB_NAME', 'myname')

                db_user = docker_config[component_type].get('WORDPRESS_DB_USER', 'myuser')

                db_password = docker_config[component_type].get('WORDPRESS_DB_PASSWORD', 'mypassword123')

                db_host = docker_config[component_type].get('WORDPRESS_DB_HOST', 'myhost')

                volume_path = docker_config[component_type].get('wp_data', '')

                wp_port = docker_config[component_type].get('port', '8080')

                restart = docker_config[component_type].get('restart', '')

                terraform_code += f'  volumes {{\n    container_path = "{volume_path}"\n}}\n'
                terraform_code += f'  restart = "{restart}"\n'
                terraform_code += (f'  env = [ "WORDPRESS_DB_NAME= {db_name}","WORDPRESS_DB_PASSWORD= {db_password}",'
                                   f'"WORDPRESS_DB_USER= {db_user}","WORDPRESS_DB_HOST= {db_host}"]\n')
                terraform_code += (f'  ports {{\n    internal = 80\n    external = '
                                   f' {wp_port}\n  }}\n')

            elif component_type == 'proxy':
                # HAProxy use case

                proxy_port = docker_config[component_type].get('proxy_port', '80')
                volume_path = docker_config[component_type].get('volume', '')
                config_file = docker_config[component_type].get('config_file', '')
                MAXCONN = docker_config[component_type].get('MAXCONN', '')
                MODE = docker_config[component_type].get('MODE', '')
                HTTP_CHECK = docker_config[component_type].get('HTTP_CHECK', '')
                STATS_PORT = docker_config[component_type].get('STATS_PORT', '')
                STATS_AUTH = docker_config[component_type].get('STATS_AUTH', '')
                TIMEOUT_CONNECT = docker_config[component_type].get('TIMEOUT_CONNECT', '')
                TIMEOUT_CLIENT = docker_config[component_type].get('TIMEOUT_CLIENT', '')
                TIMEOUT_SERVER = docker_config[component_type].get('TIMEOUT_SERVER', '')
                terraform_code += (f'  volumes {{\n    host_path      = "{config_file}"\n    '
                                   f'container_path ="{volume_path}"\n    '
                                   f'read_only = "true"\n}}\n')
                terraform_code += (f'  ports {{\n    internal = {proxy_port}\n    external = '
                                   f'8080\n  }}\n')
                terraform_code += (f'  env = [ "MAXCONN= {MAXCONN}","MODE= {MODE}",'
                                   f'"HTTP_CHECK= {HTTP_CHECK}","STATS_PORT= {STATS_PORT}",'
                                   f'"STATS_AUTH= {STATS_AUTH}","TIMEOUT_CONNECT= {TIMEOUT_CONNECT}",'
                                   f'"TIMEOUT_CLIENT= {TIMEOUT_CLIENT}","TIMEOUT_SERVER= {TIMEOUT_SERVER}"]\n')
            # ################## DA QUI IN POI TUTTO DA TESTARE ######################################
            elif component_type == 'monitoring':
                # Prometheus & Grafana (Monitoraggio e Registrazione)
                prometheus_port = docker_config[component_type].get('prometheus_port', '9090')
                grafana_port = docker_config[component_type].get('grafana_port', '3000')
                terraform_code += (f'  ports {{\n    internal = {prometheus_port}\n    external = '
                                   f' {prometheus_port}\n  }}\n')
                terraform_code += (f'  ports {{\n    internal = {grafana_port}\n    external = '
                                   f' {grafana_port}\n  }}\n')

            elif component_type == 'ci_cd':
                # Jenkins use case (Continuous Integration / Continuous Deployment)
                jenkins_port = docker_config[component_type].get('port', '8080')
                terraform_code += (f'  ports {{\n    internal = {jenkins_port}\n    external = '
                                   f' {jenkins_port}\n  }}\n')

            elif component_type == 'e_commerce':
                # Magento use case
                magento_port = docker_config[component_type].get('port', '8080')
                terraform_code += (f'  ports {{\n    internal = {magento_port}\n    external = '
                                   f' {magento_port}\n  }}\n')

            elif component_type == 'machine_learning':
                # Jupyter Notebook use case
                jupyter_port = docker_config[component_type].get('port', '8888')
                terraform_code += (f'  ports {{\n    internal = {jupyter_port}\n    external = '
                                   f' {jupyter_port}\n  }}\n')

            elif component_type == 'version_control':
                # GitLab use case
                gitlab_port = docker_config[component_type].get('port', '80')
                terraform_code += (f'  ports {{\n    internal = {gitlab_port}\n    external = '
                                   f' {gitlab_port}\n  }}\n')

            terraform_code += '}\n\n'

    print("Terraform plan generated.")
    return terraform_code
