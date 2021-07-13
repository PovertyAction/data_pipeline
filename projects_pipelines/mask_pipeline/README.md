
1. Log into server

`ssh -i /path/to/pem/key/pem_key.pem ubuntu@ec2_instance_dns`

1. Clone repo

`git clone https://github.com/PovertyAction/surveycto_data_download.git1`

2. Install python3-venv, create venv inside project folder, activate and install dependencies

`sudo apt-get install python3-venv`

`python3 -m venv venv`

`source venv/bin/activate`

`git install -r requirements.txt`

3. Copy credentials to server

From local machine, copy box credentials to server

`scp -i /masks-project-key.pem surveycto_data_download/box/jwt_config_file.json ubuntu@ec2_instance_dns:~/surveycto_data_download/box`
