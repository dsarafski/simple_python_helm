FROM python:3.7.3-alpine3.9 as prod

RUN mkdir /app/
WORKDIR /app/

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./simple_scrape.py /app/

CMD python3 simple_scrape.py