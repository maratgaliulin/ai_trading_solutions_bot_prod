FROM python:3.10.11
WORKDIR /root
COPY . /root
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["python3", "main.py"]


FROM python:3.10.11
WORKDIR /root
CMD ["python3", "run_parser.py"]