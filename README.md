Item Inventory Manager
======================

### How to run it
1. Git clone project.
2. Install docker.io - https://docs.docker.com/installation/ubuntulinux/.
  1. On Ubuntu 14.04 or above it should be as simple as ```sudo apt-get install docker.io```.
3. From the project root folder, run ```make run```. It might ask for your password, as docker requires sudo access.
4. Access application via [http://localhost:5001/](http://localhost:5001/).
5. Once finished, run ```make clean clean_docker``` to remove any traces.

### Features
- Python Flask backend with REST api. Uses sqlite3 to store data.
- Node.js Express frontend. Uses bootstrap for simple styling.
- Backend and frontend run in isolated Centos7 docker containers.

### Quirks
- Frontend is not tested and has poor error handling :(
- Backend is missing json schema validation.
- You need to create a Room before being able to add Items to it.
- The frontend does not allow you to delete Rooms and Items. However this can be done using the REST api.
