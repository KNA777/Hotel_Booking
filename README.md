git config --local user.name "Nikita Karyakin"
git config --local user.email "dragunov24@mail.ru"

#DOCKER NETWORK CREATE
docker network create myNetwork

#POSTGRES DB
docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=adcd \
    -e POSTGRES_PASSWORD=adcde \
    -e POSTGRES_DB=booking \
    --network=myNetwork \
    --volume pg-booking-data:/var/lib/postgres/data \
    -d postgres:17

#REDIS
docker run --name booking_cache -p 7379:6379 --network=myNetwork -d redis:7.4

#BACKEND
docker run --name booking_back -p 8888:8000 --network=myNetwork booking_img

#CELERY WORKER
docker run --name booking_celery_worker --network=myNetwork booking_img celery -A src.tasks.celery_app:celery_instance worker -l INFO --pool=solo

#CELERY BEAT
docker run --name booking_celery_worker --network=myNetwork booking_img celery -A src.tasks.celery_app:celery_instance beat -l INFO

#NGINX
docker run --name booking_nginx --volume "$PWD/nginx.conf:/etc/nginx/nginx.conf" --volume /etc/letsencrypt:/etc/letsencrypt --volume /var/lib/letsencrypt:/var/lib/letsencrypt --network=myNetwork --rm -p 443:443 nginx

#CI/CD GITLAB RUNNER
docker run -d --name gitlab-runner --restart always \
  -v /srv/gitlab-runner/config:/etc/gitlab-runner \
  -v /var/run/docker.sock:/var/run/docker.sock \
  gitlab/gitlab-runner:alpine


#REGISTRATION RUNNER
docker run --rm -it \
    -v /srv/gitlab-runner/config:/etc/gitlab-runner \
    gitlab/gitlab-runner:alpine register











