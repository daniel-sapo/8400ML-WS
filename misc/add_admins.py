import subprocess
import shlex

def add_admin_users(file_path, config_path):
    with open(file_path, 'r') as file:
        user_names = [line.strip() for line in file.readlines() if line.strip()]

    admin_users_line = f"c.Authenticator.admin_users = {set(user_names)}\n"

    with open(config_path, 'r') as file:
        config_lines = file.readlines()

    config_lines = [line for line in config_lines if not line.startswith('c.Authenticator.admin_users =')]

    config_lines.append(admin_users_line)

    with open(config_path, 'w') as file:
        file.writelines(config_lines)

    for user_name in user_names:
        try:
            subprocess.run(['sudo', 'adduser', '--disabled-password', '--force-badname', '--gecos', '""', user_name], check=True)

            subprocess.run(f'echo {user_name}:8400 | sudo chpasswd', shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while creating or setting password for user {user_name}: {e}")

    print(f"Updated admin users in the config: {config_path} and created system users.")

users_file_path = 'users.txt'
config_file_path = '/home/ubuntu/setup/jupyterhub_config.py'

add_admin_users(users_file_path, config_file_path)