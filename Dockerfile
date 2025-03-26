FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY wc_api.py .
CMD ["python", "wc_api.py"]