FROM python:3.9
EXPOSE 8000
RUN ["pip", "install", "--no-cache-dir", "poetry"]
WORKDIR /app
COPY . .
RUN ["rm", ".env"]
RUN ["poetry", "install"]
CMD ["poetry", "run", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]