# parent image
FROM python:3.12-slim

WORKDIR /app

# copy environment file 
COPY environment.yml .
# install dependencies
RUN pip install --no-cache-dir -r environment.yml

# copy model files and scoring script into the container
COPY . .

EXPOSE 5000

# entrypoint
CMD ["python", "score.py"]
