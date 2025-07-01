FROM python:3.13

WORKDIR /WORKDIR


COPY app ./app
COPY ./alembic.ini .
COPY alembic ./alembic
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
