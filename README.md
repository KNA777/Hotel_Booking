

docker network create myNetwork

docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=adcd \
    -e POSTGRES_PASSWORD=adcde \
    -e POSTGRES_DB=booking \
    --network=myNetwork \
    --volume pg-booking-data:/var/lib/postgres/data \
    -d postgres:17


docker run --name booking_cache -p 7379:6379 --network=myNetwork -d redis:7.4

docker run --name booking_back -p 8888:8000 --network=myNetwork booking_img

docker run --name booking_celery_worker --network=myNetwork booking_img celery -A src.tasks.celery_app:celery_instance worker -l INFO --pool=solo

docker run --name booking_celery_worker --network=myNetwork booking_img celery -A src.tasks.celery_app:celery_instance beat -l INFO