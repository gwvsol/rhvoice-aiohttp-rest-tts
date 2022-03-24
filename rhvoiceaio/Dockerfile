# Какой используем образ
FROM debian:bullseye-slim
LABEL maintainer="Mikhail Fedorov" email="jwvsol@yandex.ru"
LABEL version="latest"

ARG USER_ID
ENV USER_ID ${USER_ID:-1000}
ARG GROUP_ID
ENV GROUP_ID ${GROUP_ID:-1000}
ARG TIMEZONE
ENV TIMEZONE=${TIMEZONE:-Europe/Moscow}

# Используется в некоторых случаях если не возможно собрать образ
#ENV HTTP_PROXY="http://192.168.93.1:3128"
#ENV HTTPS_PROXY="https://192.168.93.1:3128"

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Переменная оболочки 
ENV SHELL=/bin/bash

# Имя релиза приложения
ENV APPS=rhvoiceaio

# Директория для запуска сервиса
ENV APP_DIR=/usr/src

# Создаем не привилигированного пользователя для работы приложения
RUN groupadd --gid ${GROUP_ID} $APPS \
    && useradd --uid ${USER_ID} --gid $APPS --shell $SHELL --create-home $APPS

# Устанавливаем временную зону и локализацию
RUN ln -snf /usr/share/zoneinfo/$TIMEZONE /etc/localtime && echo $TIMEZONE > /etc/timezone \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get -y install locales procps \
    && sed -i '/ru_RU.UTF-8/s/^# //g' /etc/locale.gen && locale-gen

# Устанавливаем локаль RU.UTF-8
ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8

# Устанавливаем необходимые пакеты и зависимости
RUN apt-get install -y build-essential git make unzip tzdata curl \
       libspeechd-dev lame opus-tools flac \
    && apt-get install -y python3 python3-dev python3-pip \
       python3-venv python3-setuptools python3-wheel \
    && pip3 install scons lxml setuptools wheel \
    && apt-get clean \
    && rm -rf /root/.cache/pip

# Копируем релиз в Docker
COPY release/${APPS}-*.zip /tmp/

# Установка зависимостей и приложения
RUN set -eux \
    && mkdir -p ${APP_DIR} \
    && mv /tmp/${APPS}-*.zip $APP_DIR \
    && cd ${APP_DIR} \
    && unzip ${APPS}-*.zip \
    && rm *.zip \
    && chown -Rf $APPS:$APPS $APP_DIR

# Переключаем на не привилигированного пользователя
USER $APPS
# Переключаем на диреторию в которой будет работать приложение
WORKDIR $APP_DIR

# Запускаем установку приложения
RUN make install-rhvoiceaio \
    && rm -fr .env \
    && rm -rf $HOME/.cache/pip

# Устанавливаем проверку работы приложения
HEALTHCHECK --interval=180s \
            --timeout=1s \
            --retries=3 \
            --start-period=10s \
            CMD curl --fail -X GET http://localhost:8040 || kill 1

# Открываем порты
EXPOSE 8040

# Что стартуем при запуске Docker
ENTRYPOINT ["make", "run-rhvoiceaio"]
