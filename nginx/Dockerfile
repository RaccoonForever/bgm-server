FROM nginx:1.19.0

RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/

RUN rm /etc/nginx/conf.d/default.conf
COPY bgm_server.conf /etc/nginx/conf.d/

COPY ./static ./static
