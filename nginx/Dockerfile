FROM nginx:1.19.0

RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/nginx.conf

RUN rm /etc/nginx/conf.d/default.conf
COPY bgm_server.conf /etc/nginx/conf.d/bgm_server.conf

COPY ./static ./static
