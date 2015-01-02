# 
# Stand-alone tesseract-ocr web service in python.
# 
# Version: 0.0.2 
# Developed by Mark Peng (markpeng.ntu at gmail)
# 

FROM ubuntu:12.04

MAINTAINER guitarmind

RUN apt-get update && apt-get install -y \
  autoconf \
  automake \
  autotools-dev \
  build-essential \
  checkinstall \
  libjpeg-dev \
  libpng-dev \
  libtiff-dev \
  libtool \
  python \
  python-imaging \
  python-tornado \
  wget \
  zlib1g-dev

RUN mkdir ~/temp \
  && cd ~/temp/ \
  && wget http://www.leptonica.org/source/leptonica-1.69.tar.gz \
  && tar -zxvf leptonica-1.69.tar.gz \
  && cd leptonica-1.69 \
  && ./configure \
  && make \
  && checkinstall \
  && ldconfig

RUN cd ~/temp/ \
  && wget https://tesseract-ocr.googlecode.com/files/tesseract-ocr-3.02.02.tar.gz \
  && tar xvf tesseract-ocr-3.02.02.tar.gz \
  && cd tesseract-ocr \
  && ./autogen.sh \
  && mkdir ~/local \
  && ./configure --prefix=$HOME/local/ \
  && make \
  && mkdir ~/local/share \
  && cd ~/local/share \
  && wget https://tesseract-ocr.googlecode.com/files/tesseract-ocr-3.02.eng.tar.gz \
  && tar xvf tesseract-ocr-3.02.eng.tar.gz

ENV TESSDATA_PREFIX /root/local/share/tesseract-ocr

RUN mkdir -p /opt/ocr/static

COPY tesseractcapi.py /opt/ocr
COPY tesseractserver.py /opt/ocr

RUN chmod 755 /opt/ocr/*.py 

EXPOSE 8080

WORKDIR /opt/ocr

CMD ["python", "/opt/ocr/tesseractserver.py", "-p", "8080", "-b", "\"/root/local/lib\"", "-d", "\"/root/local/share/tesseract-ocr\"" ]

