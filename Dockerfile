FROM python:3.13

WORKDIR /WORKDIR


COPY app ./app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
