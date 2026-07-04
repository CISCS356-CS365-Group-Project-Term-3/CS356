FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./user_management

ENV UVICORN_HOST=0.0.0.0
ENV UVICORN_PORT=5000

CMD ["sh", "-c", "python -m uvicorn user_management.api.user_portal_controller:app --host \"$UVICORN_HOST\" --port \"$UVICORN_PORT\""]
