

# start the demo w/ docker compose
# docker compose restart data-generator-fluvio-client seems to sometimes be needed
start:
	docker compose up --detach
	echo Access 127.0.0.1:8000 to view the sdf studio ui
	echo Access 127.0.0.1:3001 to view the demo dashboard

stop:
	docker compose down -v

# after dockerfile updates, starting w/ --build may be required
# slow as this reubuilds images
# docker compose up --build --no-deps SERVICE may also be useful
fresh-start:
	docker compose up --build --detach

# Install sdf-beta3 locally as a client
install:
	UN curl -fsS "https://hub.infinyon.cloud/install/install.sh?ctx=ga-sdf-demo" | FLUVIO_VERSION=sdf-beta3 bash

# show graphical UI of the dataflow
studio:
	sdf deploy --ui
