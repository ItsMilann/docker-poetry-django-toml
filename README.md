## Create necessary files
some configuration can change depending upon the running environment or the project
for that purpose example of configurable files pushed rather than actual configuration.

make a copy of `env.txt.example`, `docker-compose.example.yml`, `project/uwsgi.ini.example`

```
cp env.txt.example env.txt 
cp docker-compose.example.yml docker-compose.yml
cp project/uwsgi.ini.example project/uwsgi.ini
```
## Build image
Use docker build command to build a image of the project

```bash
sudo docker build -t <image_name>:<tag> project
# example:
sudo docker build -t boilerplate:0.0.1 project
```

## Usage
Start the services in detached mode
```bash
sudo docker-compose up -d
```
## Access the Running Container
To access a running container, use the following command:

```bash
sudo docker exec -it <container-name> bash
# example:
sudo docker exec -it backends bash
```