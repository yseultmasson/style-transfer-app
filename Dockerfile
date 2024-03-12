FROM python:3.9.4
WORKDIR /mise-en-production

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .
COPY src ./src
COPY static ./static

EXPOSE 8000

CMD ["streamlit", "run", "app.py", "--server.port=8000", "--server.address=0.0.0.0"]