FROM python:3.12-slim

WORKDIR /usr/src/app


COPY requirements_db.txt ./
RUN pip install --no-cache-dir -r requirements_db.txt

COPY . .

CMD ["python3", "query_llm.py"]
