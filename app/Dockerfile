FROM python:3.10.1-buster

MAINTAINER https://github.com/njdowdy

ENV POETRY_VERSION 1.1.12

RUN set -ex; pip install --no-cache-dir poetry==$POETRY_VERSION;

WORKDIR /mnt/app

#CMD ["poetry", "install"]
#CMD [ "poetry", "run", "python", "script.py" ]
CMD poetry install ; poetry run python script.py