FROM tiangolo/meinheld-gunicorn:python3.6

RUN pip3 --no-cache-dir install --upgrade pip
RUN pip3 --no-cache-dir install cert-issuer

# configure cert-issuer
RUN mkdir -p /etc/cert-issuer/
WORKDIR /app
COPY main.py /app
