dev:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 --log-config logger_config.yml 

up:
	docker compose -f ./docker/app-compose.yml -f docker/mongo-compose.yml -f docker/kafka-compose.yml up -d --build

up-dev:
	docker compose -f ./docker/dev-compose.yml -f docker/mongo-compose.yml -f docker/kafka-compose.yml up --build --abort-on-container-exit --attach dev-app --no-log-prefix

down:
	docker compose -f ./docker/app-compose.yml -f ./docker/dev-compose.yml -f docker/mongo-compose.yml -f docker/kafka-compose.yml down 
