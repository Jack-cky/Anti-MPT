# build image
docker build --no-cache --platform linux/amd64 -t jackcky/antimpt:v0 -f docker/Dockerfile .

# tag image
docker tag jackcky/antimpt:v0 jackcky/antimpt:latest

# push to Docker Hub
docker push jackcky/antimpt:latest

# run container
docker run --name antimpt --platform linux/amd64 --env-file config/.env -p 8000:8000 jackcky/antimpt:latest
