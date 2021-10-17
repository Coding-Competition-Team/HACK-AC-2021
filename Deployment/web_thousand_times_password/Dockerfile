FROM php:7.4.3-apache
RUN docker-php-ext-install mysqli pdo pdo_mysql mysqli && docker-php-ext-enable mysqli
COPY ./php.ini /usr/local/etc/php/php.ini
EXPOSE 80

# FROM ubuntu:latest
# ENV DEBIAN_FRONTEND=noninteractive
# RUN apt-get update -y
# RUN apt-get upgrade -y
# RUN apt-get install -y apache2 
# RUN apt-get install -y php 
# RUN apt-get install -y php-dev 
# RUN apt-get install -y php-mysql 
# RUN apt-get install -y libapache2-mod-php 
# RUN apt-get install -y php-curl 
# RUN apt-get install -y php-json 
# RUN apt-get install -y php-common 
# RUN apt-get install -y php-mbstring 
# RUN apt-get install -y composer
# COPY ./php.ini /etc/php/7.4/apache2/php.ini

# CMD ["apachectl","-D","FOREGROUND"]
# RUN a2enmod rewrite
# EXPOSE 80