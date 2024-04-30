FROM python:3.11

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY tables_creation.py /app/tables_creation.py
COPY main.py /app/main.py
COPY settings.py /app/settings.py

WORKDIR /app

CMD python tables_creation.py && python main.py 
# docker-compose -f docker-compose-local.yaml up -d && 