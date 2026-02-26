FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create upload directories
RUN mkdir -p app/static/uploads/gallery \
             app/static/uploads/notes \
             app/static/uploads/avatars \
             app/static/uploads/thumbnails \
             instance

# Seed database on first run
RUN python seed.py

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "run:app"]
