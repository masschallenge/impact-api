FROM nginx
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY web/impact/static /static
CMD nginx -g 'daemon off;'
