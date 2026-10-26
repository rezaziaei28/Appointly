# import python
FROM python:3.13

# Set the working directory inside the container
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements first (for better caching)
COPY requirements.txt /app/

# Install dependencies
# Use Chabokan mirror because Docker Hub and PyPI are not available in Iran
# Remove this and use the default PyPI when you have a DNS
RUN pip install --no-cache-dir -r requirements.txt \
    --index-url https://mirror2.chabokan.net/pypi/simple/ \
    --trusted-host mirror2.chabokan.net


# Copy the rest of the project
COPY core /app/

# Expose port
EXPOSE 8000

# Run Django development server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
