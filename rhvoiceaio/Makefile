#=============================================
# Определение переменных для установки и запуска RHVOICEAIO
SETUP=${SETUP_RHVOICEAIO}
# Установка приложения RHVOICEAIO
.PHONY: install-rhvoiceaio
install-rhvoiceaio: ${DEPENDENCES_RHVOICEAIO} install
	@${PIP} install pip wheel -U
	@${PIP} install --editable ${RHVOICEAIO}

# Запуск приложения RHVOICEAIO
.PHONY: run-rhvoiceaio
run-rhvoiceaio: ${SETUP_RHVOICEAIO} venv
	@${VENV_BIN}/${RHVOICEAIO}
#	@${PYTHON} -m ${RHVOICEAIO}

# Сборка RHVOICEAIO
.PHONY: build-rhvoiceaio
build-rhvoiceaio: ${DOCKER} ${DOCKERFILE_RHVOICEAIO}
	@make release
	@${DOCKER} build \
	--file ./${DOCKERFILE_RHVOICEAIO} \
	--build-arg TIMEZONE=${TIMEZONE} \
	--build-arg USER_ID=${USER_ID} \
	--build-arg GROUP_ID=${USER_ID} \
	--tag ${RHVOICEAIO}:${RELEASE_IMAGE} ./

# Cтарт RHVOICEAIO
.PHONY: start-rhvoiceaio
start-rhvoiceaio: ${DOCKER} ${DOCKERFILE_RHVOICEAIO}
	@[ `${DOCKER} ps | grep ${RHVOICEAIO} | wc -l` -eq 1 ] || \
	${COMPOSE} -f ${COMPOSE_FILE} up -d ${RHVOICEAIO}
#	${DOCKER} run \
#	--name ${RHVOICEAIO} \
#	--rm \
#	--volume ${ENVFILE}:/usr/src/.env \
#	--publish ${RHVOICEAIO_PORT}:${RHVOICEAIO_PORT} \
#	--detach ${RHVOICEAIO}:${RELEASE_IMAGE}
# 	--restart=always

# Стоп RHVOICEAIO
.PHONY: stop-rhvoiceaio
stop-rhvoiceaio: ${DOCKER} ${DOCKERFILE_RHVOICEAIO}
	@! [ `${DOCKER} ps | grep ${RHVOICEAIO} | wc -l` -eq 1 ] || \
	${DOCKER} stop ${RHVOICEAIO}

# Рестарт RHVOICEAIO
.PHONY: restart-rhvoiceaio
restart-rhvoiceaio: ${DOCKER} ${COMPOSE} ${COMPOSE_FILE} ${DOCKERFILE_RHVOICEAIO}
	@! [ `${DOCKER} ps | grep ${RHVOICEAIO} | wc -l` -eq 1 ] || \
	make stop-rhvoiceaio
	@sleep 3
	@make start-rhvoiceaio

# Удаление RHVOICEAIO
.PHONY: remove-rhvoiceaio
remove-rhvoiceaio: ${DOCKER} ${DOCKERFILE_RHVOICEAIO}
	@make stop-rhvoiceaio
	@${DOCKER} rmi ${RHVOICEAIO}:${RELEASE_IMAGE}

# Логирование RHVOICEAIO
.PHONY: log-rhvoiceaio
log-rhvoiceaio: ${DOCKER} ${COMPOSE} ${COMPOSE_FILE} ${DOCKERFILE_RHVOICEAIO} 
	@! [ `${DOCKER} ps | grep ${RHVOICEAIO} | wc -l` -eq 1 ] || \
		${DOCKER} logs --follow --tail 500 ${RHVOICEAIO}
#		${COMPOSE} -f ${COMPOSE_FILE} logs --follow --tail 500 ${RHVOICEAIO}

#=============================================

# поддерживаемые голоса и языки
.PHONY: voices
voices:
	@curl -s "http://${LOCALHOST}:${ROBOTISK_PORT}/voices" | jq '.'

# поддеоживаемые звуковые форматы
.PHONY: formats
formats:
	@curl -s "http://${LOCALHOST}:${ROBOTISK_PORT}/formats" | jq '.'

# проверка воспроизведения звука через браузер
.PHONY: play
play:
	@(xdg-open "http://${LOCALHOST}:${ROBOTISK_PORT}/say?text=привет братишка&format=mp3&voice=arina" &)

# получение информации о работе сервиса
.PHONY: info
info:
	@curl -s "http://${LOCALHOST}:${ROBOTISK_PORT}" | jq '.'

#=============================================
