FROM python:3.7

COPY requirements.txt /course-catalog/
RUN pip install -r /course-catalog/requirements.txt

COPY *.py /course-catalog/
WORKDIR /course-catalog/

CMD ["python", "get_listings.py"]
