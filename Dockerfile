FROM python:2
ENV MAINTAINER lfries

RUN mkdir app
COPY . app/
WORKDIR app/

RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt

# long timeout for long compute times
CMD ["gunicorn", "application:app", "--bind", "0.0.0.0:8000", "--workers", "1","--timeout", "200", "--log-level=debug"]