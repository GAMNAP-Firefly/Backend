FROM nginx:stable-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/
# COPY selfsigned.crt /etc/nginx/conf.d/selfsigned.crt
# COPY selfsigned.key /etc/nginx/conf.d/selfsigned.key