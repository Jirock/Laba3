FROM python:3

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

# RUN pip install Flask

EXPOSE 80

CMD [ "python3", "app.py"]