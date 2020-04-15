## Using docker-compose

### Starting and stopping
`docker-compose up --build -d`: build containers before starting
`docker-compose down`: stop containers

## Container maintenance
Get into container
`docker exec -it {container_name} sh`

Rebuild discarding EVERYTHING
`docker-compose up --build --force-recreate --no-deps`

### Logs
`docker-compose logs -f`: show all container live logs
`docker-compose logs -f {container}`: show specific container logs
