build:
	docker compose build

up:
	docker compose up -d --build

stop:
	docker compose stop

start:
	docker compose start

down:
	docker compose down

server:
	docker compose run --entrypoint "python main.py" rpc-server

client:
	docker compose run --entrypoint "python main.py" rpc-client

generation:
	docker compose run --entrypoint "python main.py" sample-xml-generation