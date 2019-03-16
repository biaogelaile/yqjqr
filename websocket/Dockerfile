FROM python:3.6.6-alpine3.8 

WORKDIR /data
RUN pip3 install  -i https://pypi.douban.com/simple flask_socketio flask requests
ADD . /data
RUN python3 setup.py sdist
RUN python3 setup.py install

#设置时区
#RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

CMD ["python3", "websocket_chat.py"]
