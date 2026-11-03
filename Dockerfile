# 1. 베이스 이미지: nginx 공식 이미지
FROM nginx:alpine

# 2. 내 웹페이지를 nginx 기본 폴더로 복사
COPY app/ /usr/share/nginx/html/

# 3. nginx는 80번 포트를 사용
EXPOSE 80