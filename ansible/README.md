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

open_parcel_map_domain=flurstuecksauskunft.oklabflensburg.pluto
glueckskarten_domain=glueckskarten.oklabflensburg.pluto
open_biotope_map_domain=biotopkarte.oklabflensburg.pluto
open_playground_map_domain=spielplatzkarte.oklabflensburg.pluto
open_recycling_map_domain=recycling.oklabflensburg.pluto
open_topo_map_domain=topografie.oklabflensburg.pluto
open_transport_map_domain=nahverkehr.oklabflensburg.pluto
open_kita_map_domain=kitas-in-flensburg.pluto
open_cultural_map_domain=knf.grain.pluto
open_school_map_domain=schulkarte.oklabflensburg.pluto
open_social_map_domain=sozialatlas.oklabflensburg.pluto
open_social_map_dev_domain=dev.sozialatlas.oklabflensburg.pluto
open_surface_map_domain=bodennutzung.oklabflensburg.pluto
open_uranus_domain=uranus.oklabflensburg.pluto
open_data_day_domain=opendataday.oklabflensburg.pluto
open_monuments_map_domain=denkmalkarte.oklabflensburg.pluto
open_trees_map_domain=baumkarte.oklabflensburg.pluto
open_uranus_admin_domain=admin.uranus.oklabflensburg.pluto
open_uranus_api_domain=api.uranus.oklabflensburg.pluto
open_data_api_domain=api.oklabflensburg.pluto
open_gauge_map_domain=pegelstand.oklabflensburg.pluto
open_accident_map_domain=unfallkarte.oklabflensburg.pluto
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
