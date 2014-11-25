.PHONY: clean clean_docker test run

clean:
	cd backend; make clean

clean_docker:
	cd backend; make clean_docker
	- sudo docker rmi centos:centos7

test:
	cd backend; make test

run:
	cd backend; make run