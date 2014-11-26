.PHONY: clean clean_docker test build_container run

clean:
	

clean_docker:
	- sudo docker stop frontend
	- sudo docker rm frontend
	- sudo docker rmi oliviervg1/frontend

test:
	

build_container:
	dpkg -s docker.io >/dev/null 2>&1 || sudo apt-get install docker.io -y
	sudo docker build --rm -q -t="oliviervg1/frontend" .

run: clean clean_docker test build_container
	sudo docker run --name="frontend" -d -p 5001:5001 oliviervg1/frontend