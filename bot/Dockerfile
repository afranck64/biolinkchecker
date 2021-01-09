# syntax = docker/dockerfile:experimental
FROM python:3.8-slim-buster

RUN apt update && apt install git cron -y
ENV PYHTONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD ./requirements.txt /code
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

COPY . /code

ENV CRON_SCHEDULE_FETCH "0 */12 */1 * *"
ENV CRON_SCHEDULE_CHECK "15 */4 */1 * *"
ENV CRON_SCHEDULE_NOTIFY "30 */4 */1 * *"
ENV CRON_SCHEDULE_CHECK_NOTIFY "15 */4 */1 * *"
ENV CHECK_NOTIFY 1
ENV SQLALCHEMY_DATABASE_URI "sqlite://"
ENV LINKS_TTL 172800

# Run the command on container startup
CMD [sh /code/bot/entrypoint.sh]