# Blueprint to deploy node on packet.net

## Blueprint description
This AYS repo use AYS 8.2, make sure you are on the correct branch.

- server.yaml:
  contains the packet.net token and the sshkey to authorize on the server and the description of the server you want to deploy
  **Make sure you replace the token with your private token from the packet.net portal.**
- 2_g8os.yaml:
  contain the description of the g8os node and the creation of a container running ubuntu16.04 and connected to a zeotier network.
  **Make sure you configure the zerotier network ID in this blueprint**


### requirements
you need to have the AYS templates from https://github.com/g8os/ays_template_g8os.  
Just clone this repo locally before starting AYS and the templates will be availables.

make sure you have packet.net python client installed
```
pip3 install git+https://github.com/gigforks/packet-python.git --upgrade
```
#### deploying a packet.net server

In This ays repo do
```shell
# execute the first blueprint
ays blueprint 1_server.yaml
# execute the run
ays run create --follow
```

Once the run is done, your node is ready.

Inpsect the node service to get the IP address of the server:
```shell
ays service show -r node -n main


---------------------------------------------------
Service: main - Role: node
state : ok
key : 759a3405085755fd3ca9a589cda15f99

Instance data:
- client : zaibon
- deviceId : 6e67c0d1-94f6-4342-9e47-330371879e90
- deviceName : main
- deviceOs : custom_ipxe
- ipPublic : 147.75.101.117
- ipxeScriptUrl : https://stor.jumpscale.org/public/ipxe/g8os-0.12.0-generic.efi
- location : amsterdam
- planType : Type 0
- ports : ['22:22']
- projectName : kdstest
- sshLogin : root
- sshkey : packetnet

Parent: None

Children: None

Producers:
sshkey!packetnet
packetnet_client!zaibon

Consumers: None

Recurring actions: None

Event filters: None
```

#### installing the g8os node on top of the packet.net server
With the IP address of the server you got from the previous step, update the blueprint `2_g8os.yaml`

```yaml
g8os_client__main:
  redisAddr: 'PUT THE IP HERE'
```

Then execute the blueprint and create a run:
```shell
# execute the first blueprint
ays blueprint 2_g8os.yaml
# execute the run
ays run create --follow
```

Your container should be now running, you can inspect it to see it's zerotier IP
```shell
ays service show -r container

Service: ubuntu2 - Role: container
state : ok
key : 64cc03d7bbe7317e1a5fc88a231bcd01

Instance data:
- hostname : ubuntu2
- id : 1
- node : ubuntu
- zerotierID : e5cd7a9e1c0270be
- zerotierIP : 192.168.193.120

Parent:
node!ubuntu

Children: None

Producers:
node!ubuntu

Consumers: None

Recurring actions:
monitor: period:1.0 minutes last run:2017/03/18 12:03:51

Event filters: None
```
