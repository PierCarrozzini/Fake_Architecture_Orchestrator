def generate_terraform_plan(components, docker_config):
    print("Generating Terraform plan...")

    terraform_code = ""
    external_port_web_server = 8079
    port_database = 3305

    for component in components:
        component_type = component['type']
        container_name = f"{component['type']}_{component['number']}_container"
        # internal_port = component['Internal_port']

        if component_type in docker_config:
            docker_image = docker_config[component_type].get('image', 'default_docker_image')
            terraform_code += f'''
resource "docker_container" "{container_name}" {{
  image = "{docker_image}"
  name  = "{container_name}"
'''

            # Particular configurations based on component type
            if component_type == 'web_server':
                # Nginx Web server use case

                external_port_web_server += 1
                volume_path = docker_config[component_type].get('volume', '')
                terraform_code += (f'  volumes {{\n    host_path      = "{volume_path}"\n    container_path = '
                                   f'"/usr/share/nginx/html"\n  }}\n')
                terraform_code += (f'  ports {{\n    internal = 80\n    external = '
                                   f'{external_port_web_server}\n  }}\n')

            elif component_type == 'database':
                # MySQL database use case

                db_name = docker_config[component_type].get('name', 'database')

                db_user = docker_config[component_type].get('user', 'user')

                db_password = docker_config[component_type].get('password', 'password123')

                port_database += 1

                volume_path = docker_config[component_type].get('db_data', '')

                restart = docker_config[component_type].get('restart', '')

                terraform_code += f'  volumes {{\n    container_path = "{volume_path}"\n}}\n'
                terraform_code += f'  restart = "{restart}"\n'
                terraform_code += (f'  env = [ "MYSQL_DATABASE= {db_name}","MYSQL_ROOT_PASSWORD= {db_password}",'
                                   f'"MYSQL_USER= {db_user}","MYSQL_PASSWORD= {db_password}"]\n')
                terraform_code += (f'  ports {{\n    internal = {port_database}\n    external = '
                                   f' {port_database}\n  }}\n')

            elif component_type == 'firewall-alpine':
                # API-Firewall use case

                firewall_port = docker_config[component_type].get('port', '8088')
                restart = docker_config[component_type].get('restart', '')
                host_path_to_spec = docker_config[component_type].get('HOST_PATH_TO_SPEC', 'LOG_ONLY')
                container_path_to_spec = docker_config[component_type].get('CONTAINER_PATH_TO_SPEC', 'LOG_ONLY')
                apifw_request_validation = docker_config[component_type].get('APIFW_REQUEST_VALIDATION', 'LOG_ONLY')
                apifw_response_validation = docker_config[component_type].get('APIFW_RESPONSE_VALIDATION', 'LOG_ONLY')
                apifw_api_specs = docker_config[component_type].get('APIFW_API_SPECS', '')
                apifw_url = docker_config[component_type].get('APIFW_URL', '')
                apifw_server_url = docker_config[component_type].get('APIFW_SERVER_URL', '')

                # terraform_code += f'  volumes {{\n   <{host_path_to_spec}> = "<{container_path_to_spec}>"\n}}\n'
                terraform_code += (f'  ports {{\n    internal = {firewall_port}\n    external = '
                                   f' {firewall_port}\n  }}\n')
                terraform_code += f'  restart = "{restart}"\n'
                terraform_code += (f'  env = [ "APIFW_REQUEST_VALIDATION= {apifw_request_validation}", '
                                   f'"APIFW_RESPONSE_VALIDATION= {apifw_response_validation}", "APIFW_API_SPECS= '
                                   f'{apifw_api_specs}"]\n')
            # "APIFW_URL= {apifw_url}", "APIFW_SERVER_URL= {apifw_server_url}"

            elif component_type == 'firewall':
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
                redis_password = docker_config[component_type].get('REDIS_PASSWORD', 'password123')
                redis_maxmemory = docker_config[component_type].get('REDIS_MAXMEMORY', '50mb')
                redis_appendonly = docker_config[component_type].get('REDIS_APPENDONLY', 'yes')

                terraform_code += (f'  ports {{\n    internal = {cache_port}\n    external = '
                                   f' {cache_port}\n  }}\n')
                terraform_code += f'  restart = "{restart}"\n'
                # terraform_code += f' command = "{command}"\n'
                terraform_code += (
                    f'  env = [ "REDIS_PASSWORD= {redis_password}", "REDIS_MAXMEMORY= {redis_maxmemory}",'
                    f'"REDIS_APPENDONLY= {redis_appendonly}"]\n')

            elif component_type == 'message_queque':
                # RabbitMQ message queue use case

                mq_port = docker_config[component_type].get('port', '5672')
                restart = docker_config[component_type].get('restart', '')
                rabbitmq_default_vhost = docker_config[component_type].get('RABBITMQ_DEFAULT_VHOST', '/')
                rabbitmq_default_user = docker_config[component_type].get('RABBITMQ_DEFAULT_USER', 'myuser')
                rabbitmq_default_pass = docker_config[component_type].get('RABBITMQ_DEFAULT_PASS', 'mypass')

                terraform_code += (f'  ports {{\n    internal = {mq_port}\n    external = '
                                   f' {mq_port}\n  }}\n')
                terraform_code += f'  restart = "{restart}"\n'
                # terraform_code += f' command = "{command}"\n'
                terraform_code += (f'  env = [ "RABBITMQ_DEFAULT_VHOST= {rabbitmq_default_vhost}",'
                                   f' "RABBITMQ_DEFAULT_USER= {rabbitmq_default_user}",'
                                   f' "RABBITMQ_DEFAULT_PASS= {rabbitmq_default_pass}"]\n')

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
                maxconn = docker_config[component_type].get('MAXCONN', '')
                mode = docker_config[component_type].get('MODE', '')
                http_check = docker_config[component_type].get('HTTP_CHECK', '')
                stats_port = docker_config[component_type].get('STATS_PORT', '')
                stats_auth = docker_config[component_type].get('STATS_AUTH', '')
                timeout_connect = docker_config[component_type].get('TIMEOUT_CONNECT', '')
                timeout_client = docker_config[component_type].get('TIMEOUT_CLIENT', '')
                timeout_server = docker_config[component_type].get('TIMEOUT_SERVER', '')
                terraform_code += (f'  volumes {{\n    host_path      = "{config_file}"\n    '
                                   f'container_path ="{volume_path}"\n    '
                                   f'read_only = "true"\n}}\n')
                terraform_code += (f'  ports {{\n    internal = {proxy_port}\n    external = '
                                   f'{proxy_port}\n  }}\n')
                terraform_code += (f'  env = [ "MAXCONN= {maxconn}","MODE= {mode}",'
                                   f'"HTTP_CHECK= {http_check}","STATS_PORT= {stats_port}",'
                                   f'"STATS_AUTH= {stats_auth}","TIMEOUT_CONNECT= {timeout_connect}",'
                                   f'"TIMEOUT_CLIENT= {timeout_client}","TIMEOUT_SERVER= {timeout_server}"]\n')

            elif component_type == 'prometheus':
                # Prometheus (Monitoraggio)
                prometheus_port = docker_config[component_type].get('prometheus_port', '9090')
                terraform_code += (f'  ports {{\n    internal = {prometheus_port}\n    external = '
                                   f' {prometheus_port}\n  }}\n')

            elif component_type == 'grafana':
                # Grafana (Registrazione)
                grafana_port = docker_config[component_type].get('grafana_port', '3000')
                terraform_code += (f'  ports {{\n    internal = {grafana_port}\n    external = '
                                   f' {grafana_port}\n  }}\n')

            elif component_type == 'machine_learning':
                # Jupyter Notebook use case

                jupyter_port = docker_config[component_type].get('port', '8888')
                jupyter_enable_lab = docker_config[component_type].get('JUPYTER_ENABLE_LAB', 'yes')
                command = docker_config[component_type].get('command', '')

                terraform_code += (f'  ports {{\n    internal = {jupyter_port}\n    external = '
                                   f' {jupyter_port}\n  }}\n')
                terraform_code += f'  env = [ "JUPYTER_ENABLE_LAB= {jupyter_enable_lab}"]\n'
                terraform_code += f' command = ["start-notebook.sh", "--NotebookApp.token=''", "--NotebookApp.password=''"]\n'

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

            elif component_type == 'version_control':
                # GitLab use case

                gitlab_port = docker_config[component_type].get('port', '80')
                terraform_code += (f'  ports {{\n    internal = {gitlab_port}\n    external = '
                                   f' {gitlab_port}\n  }}\n')

            terraform_code += '}\n\n'

    print("Terraform plan generated.")
    return terraform_code
