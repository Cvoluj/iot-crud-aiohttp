DC = docker compose
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker_compose/app.yaml
APP_CONTAINER = iot-crud

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down

.PHONY: app-shell
app-shell:
	${DC} -f ${APP_FILE} exec

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f