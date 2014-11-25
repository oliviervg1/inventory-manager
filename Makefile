.PHONY: test test_backend clean clean_docker build_containers run

################## VENV ##################
venv: backend/venv/bin/activate

backend/venv/bin/activate: backend/requirements.txt
	dpkg -s python-virtualenv >/dev/null 2>&1 || sudo apt-get install python-virtualenv -y
	test -d backend/venv || virtualenv --no-site-packages backend/venv
	cd backend; . venv/bin/activate && pip install -r requirements.txt && pip install nose
	cd backend; touch venv/bin/activate

################## CLEAN ##################
clean: clean_docker
	- rm -rf backend/venv
	- find . -name "*.pyc" | xargs rm

clean_docker:
	- sudo docker stop backend
	- sudo docker rm backend
	- sudo docker rmi oliviervg1/backend
	- sudo docker rmi centos:centos7

################## TEST ##################
test_backend: venv
	cd backend; . venv/bin/activate && nosetests -v test

test: test_backend

################## BUILD ##################
build_containers:
	dpkg -s docker.io >/dev/null 2>&1 || sudo apt-get install docker.io -y
	cd backend; sudo docker build --rm -q -t="oliviervg1/backend" .

################## RUN ##################
run: clean test build_containers
	sudo docker run --name="backend" -d -p 5000:5000 oliviervg1/backend