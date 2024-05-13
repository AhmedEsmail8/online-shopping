FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY api.py DataBaseManagement.py Models.py users_database.db /app/
EXPOSE 80
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8001"]