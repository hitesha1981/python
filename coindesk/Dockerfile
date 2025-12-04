FROM python:3.14-slim


ENV APP_PORT=8000
ENV DJANGO_HOST=0.0.0.0

# Create a user named coindesk
RUN useradd -ms /bin/bash coindesk

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
RUN mkdir -p /app/static
COPY ./ /app

# Set the working directory
WORKDIR /app

# Change ownership of the app directory to the coindesk user
RUN chown -R coindesk:coindesk /app

# Switch to the coindesk user
USER coindesk

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD python manage.py runserver ${DJANGO_HOST}:${APP_PORT}