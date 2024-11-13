

# start the demo w/ docker compose
# docker compose restart data-generator-fluvio-client seems to sometimes be needed
start:
	docker compose up --detach

stop:
	docker compose down -v

# after dockerfile updates, starting w/ --build may be required
# slow as this reubuilds images
fresh-start:
	docker compose up --build --detach
