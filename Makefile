.PHONY: clean clean_docker test run

clean:
	cd backend; make clean
	cd frontend; make clean

clean_docker:
	cd backend; make clean_docker
	cd frontend; make clean_docker
	- sudo docker rmi centos:centos7

test:
	cd backend; make test
	cd frontend; make test

run:
	cd backend; make run
	cd frontend; make run
