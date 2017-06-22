FROM nginx
COPY nginx/nginx.conf /etc/nginx/nginx.conf
ADD web/impact/static-compiled /static
CMD nginx -g 'daemon off;'
