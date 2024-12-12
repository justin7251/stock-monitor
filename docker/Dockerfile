# Base Image
FROM python:3.11-slim-bullseye

# Maintainer Information
LABEL maintainer="your_email@example.com"

# Environment Variables
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/app

# Expose Port
EXPOSE 5000

# Set Work Directory
WORKDIR $APP_HOME

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    cron gcc build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Application Files
COPY . .

# Configure Cron Job
# Copy cron job script
COPY cron_jobs/cron_script.sh /etc/cron.hourly/
RUN chmod +x /etc/cron.hourly/cron_script.sh

# Setup cron
RUN echo "SHELL=/bin/bash\n\
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin\n\
# Run cron job every hour\n\
0 * * * * /bin/bash /etc/cron.hourly/cron_script.sh >> /var/log/cron.log 2>&1" > /etc/cron.d/my-cron

# Apply cron job
RUN crontab /etc/cron.d/my-cron

# Start cron and Flask app
CMD ["sh", "-c", "service cron start && flask run --host=0.0.0.0"]
