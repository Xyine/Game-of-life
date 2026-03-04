FROM python:3.12-slim

WORKDIR /GAME_OF_LIFE

COPY requirements.txt /GAME_OF_LIFE/

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

COPY . /GAME_OF_LIFE/

ENV TERM=xterm

ENTRYPOINT ["python", "-m", "main", "terminal"]
