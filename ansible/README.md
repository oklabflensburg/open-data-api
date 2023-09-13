# Ansible Setup


Install system dependencies

```
sudo apt install ansible
```


Create a `hosts.ini` file inside the ansible directory

```
[app1]
127.0.0.1

[app1:vars]
ansible_port=22
ansible_user=user
ansible_ssh_user=user
ansible_ssh_private_key_file=path
```


Run ansible playbook with updated inventory

```
ansible-playbook playbook.yml
```
