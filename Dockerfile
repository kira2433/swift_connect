FROM python:3.9

WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip3 install -U pip
RUN pip3 install -r requirements.txt

# Copy app code
COPY . .

# Expose port
EXPOSE 5000

# Run the app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
