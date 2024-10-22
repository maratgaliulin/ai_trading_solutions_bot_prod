FROM python:3.10.11
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000

CMD ["python3", "main.py"]