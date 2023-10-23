FROM nginx:alpine
COPY . /usr/share/nginx/html
RUN chmod 777 /usr/share/nginx/html/index.html