# Ansible Setup


Install system dependencies

```
sudo apt install ansible
```


Make sure to add following community collections

```
ansible-galaxy collection install community.postgresql
```


Create a `hosts.ini` file with `touch hosts.ini`


If you want to run against a remote machine add following content

```
[app1]
127.0.0.1

[app1:vars]
ansible_port=22
ansible_user=user
ansible_ssh_user=user
ansible_ssh_private_key_file=path
mail_username=mail_address
mail_from=mail_address
mail_password=password
mail_server=host
mail_port=port
```


In case you want to run against `localhost` add this instead

```
[app1]
127.0.0.1

[app1:vars]
ansible_connection=local
```


Run ansible playbook with updated inventory

```
ansible-playbook playbook.yml -i hosts.ini
```
