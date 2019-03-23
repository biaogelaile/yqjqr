#FROM python:3.6.6-alpine3.8 
FROM python:3.6.7-jessie

WORKDIR /data
RUN pip3 install  -i https://pypi.douban.com/simple socketIO-client requests

#设置时区
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone
#RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

ADD . /data
CMD ["python3", "chatbot.py"]
