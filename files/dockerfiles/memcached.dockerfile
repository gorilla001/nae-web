FROM       centos/base
RUN          yum install -y httpd
EXPOSE    80
CMD          httpd  -D