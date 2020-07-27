FROM python:3.7-alpine
USER root

ARG project_dir=/usr/local/share/docker-application/

ADD requirements.txt $project_dir
WORKDIR ${project_dir}

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
