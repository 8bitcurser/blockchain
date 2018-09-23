FROM ubuntu
RUN apt-get -y update && apt -y install python python-pip swig libpulse-dev libxml2-dev libxslt1-dev antiword poppler-utils pstotext tesseract-ocr flac ffmpeg lame libmad0 libsox-fmt-mp3 sox

RUN pip install flask requests textract

WORKDIR src
ADD src/ .
ENV  PYTHONPATH="${PYTHONPATH}:src/"

EXPOSE 5000
ENV FLASK_APP app.py
CMD flask run --host=0.0.0.0
