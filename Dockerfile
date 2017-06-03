FROM python:2
ENV MAINTAINER lfries

RUN mkdir app
COPY . app/
WORKDIR app/

RUN pip install -r requirements.txt

CMD ["gunicorn", "application:app"]