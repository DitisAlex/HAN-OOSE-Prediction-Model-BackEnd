FROM python:3
EXPOSE 5000
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
CMD python run.py
