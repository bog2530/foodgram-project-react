FROM python:3.7

WORKDIR /app

COPY requirements.txt ./

RUN python -m pip install --upgrade pip

RUN pip3 install -r requirements.txt

COPY . ./

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]