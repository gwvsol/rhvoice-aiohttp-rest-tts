#=============================================
# Общие настройки и переменные
VENV_NAME?=venv
VENV_BIN=${VENV_NAME}/bin
VENV_ACTIVATE=. ${VENV_BIN}/activate
PYTHON=${VENV_BIN}/python3
PIP=${VENV_BIN}/pip3
GUNICORN=${VENV_BIN}/gunicorn
DOCKER=$(shell which docker)
COMPOSE=$(shell which docker-compose)

ifneq ("$(wildcard $(shell which timedatectl))","")
	export TIMEZONE=$(shell timedatectl status | awk '$$1 == "Time" && $$2 == "zone:" { print $$3 }')
endif

export USER_ID=$(shell id -u `whoami`)
export PWD=$(shell pwd)

ENVIRONMENT=.env
ENVFILE=$(PWD)/${ENVIRONMENT}
ifneq ("$(wildcard $(ENVFILE))","")
    include ${ENVFILE}
    export ENVFILE=$(PWD)/${ENVIRONMENT}
endif

# =============================================
.DEFAULT: help
.PHONY: help
help:
	@echo "make install	- Installing the project" 
	@echo "make uninstall	- Deleting a project"
	@echo "make build	- Building services in Docker using Docker Compose"
	@echo "make start	- Running services in Docker using Docker Compose"
	@echo "make stop	- Stopping services in Docker using Docker Compose"
	@echo "make restart	- Restart services in Docker using Docker Compose"
	@echo "make log	- Displaying service logs in Docker using Docker Compose"
	@echo "make remove	- Deleting services in Docker"
	@exit 0

# =============================================
# Установка зависимостей
.PHONY: install
install:
	@[ -d $(VENV_NAME) ] || python3 -m $(VENV_NAME) $(VENV_NAME)
	@${PIP} install pip wheel -U

# Активация виртуального окружения
.PHONY: venv
venv: ${VENV_NAME}/bin/activate
$(VENV_NAME)/bin/activate: ${SETUP}
	@[ -d $(VENV_NAME) ] || python3 -m $(VENV_NAME) $(VENV_NAME)
	@${PIP} install pip wheel -U
	@${PIP} install -e .
	@${VENV_ACTIVATE}

# Удаление виртуального окружения
.PHONY: uninstall
uninstall:
	@make clean
	@rm -fr ${VENV_NAME}

# =============================================
# Создание релиза приложения
.PHONY: release
release: clean ${RHVOICEAIO} ${COMPOSE_FILE} ${MAKEFILE} \
				${ENVIRONMENT} ${README}
	@[ -d $(RELEASE) ] || mkdir ${RELEASE}
	@[ -d $(ARCHIVE) ] || mkdir ${ARCHIVE}
	@find "$(RELEASE)" -name '*.zip' -type f -exec mv -v -t "$(ARCHIVE)" {} +
	@zip -r ${RELEASE}/${RHVOICEAIO}-$(shell date '+%Y-%m-%d-%H-%M-%S').zip \
	${RHVOICEAIO} ${COMPOSE_FILE} ${MAKEFILE} ${ENVIRONMENT} ${README}

# =============================================
# Очистка мусора
.PHONY: clean
clean:
	@rm -fr .eggs
	@rm -fr *.egg-info
	@find . -name '.eggs' -exec rm -fr {} +
	@find . -name '*.egg-info' -exec rm -fr {} +
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

# =============================================
# Работа с RHVOICEAIO
ifneq ("$(wildcard $(PWD)/$(RHVOICEAIO_MAKEFILE))","")
   include ${RHVOICEAIO_MAKEFILE}
endif

# =============================================
# Сборка RHVOICEAIO
.PHONY: build
build: ${DOCKER} ${COMPOSE} ${COMPOSE_FILE} 
	@make release
	@make build-basic
	@${COMPOSE} -f ${COMPOSE_FILE} build

# Старт RHVOICEAIO
.PHONY: start
start: ${DOCKER} ${COMPOSE} ${COMPOSE_FILE}
	@${COMPOSE} -f ${COMPOSE_FILE} up -d

# Остановка RHVOICEAIO
.PHONY: stop
stop: ${DOCKER} ${COMPOSE} ${COMPOSE_FILE}
	@${COMPOSE} -f ${COMPOSE_FILE} down

# Логирование RHVOICEAIO
.PHONY: log
log: ${DOCKER} ${COMPOSE} ${COMPOSE_FILE}
	@${COMPOSE} -f ${COMPOSE_FILE} logs --follow --tail 500

# Рестарт RHVOICEAIO
.PHONY: restart
restart: ${DOCKER} ${COMPOSE} ${COMPOSE_FILE}
	@make stop
	@sleep 3
	@make start

# Удаление RHVOICEAIO
.PHONY: remove
remove: ${DOCKER} ${COMPOSE} ${COMPOSE_FILE}
	@make stop
	@make remove-rhvoiceaio

# =============================================
