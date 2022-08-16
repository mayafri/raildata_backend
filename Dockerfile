FROM python:3.9
EXPOSE 8000
RUN ["pip", "install", "--no-cache-dir", "poetry"]
WORKDIR /app
COPY . .
RUN ["rm", "-rf", "__pycache__"]
RUN ["poetry", "install"]
