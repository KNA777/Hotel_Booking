# Сервис бронирования номеров

docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=adcd \
    -e POSTGRES_PASSWORD=adcd \
    -e POSTGRES_DB=practice \
    --network=myNetwork \
    --volume pg-data:/var/lib/postgresql/data \
    -d postgres:17
    
