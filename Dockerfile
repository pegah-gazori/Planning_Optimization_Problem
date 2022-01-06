FROM python:3.9.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /opt/planning_optimization_problem
COPY . /opt/planning_optimization_problem
WORKDIR /opt/planning_optimization_problem

COPY wait-for-it.sh /usr/wait-for-it.sh
RUN chmod +x /usr/wait-for-it.sh

RUN pip install --upgrade pip
RUN pip3.9 install -r requirements.txt

EXPOSE 8000
