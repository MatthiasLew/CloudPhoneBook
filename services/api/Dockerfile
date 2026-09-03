FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY packages/shared/ /app/packages/shared/
RUN pip install --no-cache-dir /app/packages/shared/

COPY services/api/pyproject.toml /app/
RUN pip install --no-cache-dir .

COPY services/api/app /app/app
COPY services/api/scripts /app/scripts

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
