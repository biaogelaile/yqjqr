FROM python:3.6.7-jessie 

#RUN echo "https://mirrors.aliyun.com/alpine/v3.8/main" > /etc/apk/repositories
#RUN echo "https://mirrors.aliyun.com/alpine/v3.8/community" >> /etc/apk/repositories 
WORKDIR /data
#RUN apk update && apk add gcc libc-dev pcre pcre-dev libffi-dev openssl-dev 
RUN apt-get update && apt-get install curl -y
RUN pip3 install  -i https://pypi.douban.com/simple flask_socketio flask flask_sqlalchemy sqlalchemy pymysql requests 
RUN pip3 install  -i https://pypi.douban.com/simple uwsgi socketIO-client
RUN pip3 install  -i https://pypi.douban.com/simple flask_cors


#设置时区
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone
#RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
 
ADD . /data
#CMD ["python3", "http_chat.py"]
CMD ["uwsgi", "--ini", "houtaiapi.ini"]
