# 
# Stand-alone tesseract-ocr web service in python.
# 
# Version: 0.0.3 
# Developed by Mark Peng (markpeng.ntu at gmail)
# 

FROM debian:sid

MAINTAINER guitarmind

RUN apt-get update && apt-get install -y \
  python \
  python-imaging \
  python-tornado \
  tesseract-ocr \
  tesseract-ocr-eng

ENV TESSDATA_PREFIX /usr/share/tesseract-ocr

RUN mkdir -p /opt/ocr/static

COPY tesseractcapi.py /opt/ocr/tesseractcapi.py
COPY tesseractserver.py /opt/ocr/tesseractserver.py

RUN chmod 755 /opt/ocr/*.py 

EXPOSE 1688

WORKDIR /opt/ocr

CMD ["python", "/opt/ocr/tesseractserver.py", "-p", "1688", "-b", "/usr/lib", "-d", "/usr/share/tesseract-ocr" ]
