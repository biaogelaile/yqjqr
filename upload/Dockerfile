FROM python:3.6.7-jessie
#FROM mychat/chatapi 
RUN rm -rf /data
RUN pip3 install uwsgi -i https://pypi.douban.com/simple

#设置时区
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone
#RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime


ADD . /data
#CMD ["python3", "http_chat.py"]
CMD ["uwsgi", "--ini", "upload.ini"]
