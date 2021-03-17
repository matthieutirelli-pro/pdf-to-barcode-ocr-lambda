FROM public.ecr.aws/lambda/python:3.8
RUN yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
RUN yum install -y zbar zbar-devel graphicsmagick poppler-utils
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY app.py ./
COPY scan.pdf ./
CMD ["app.handler"]
