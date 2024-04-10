architectures=linux/amd64,linux/arm64,linux/arm/v7,linux/arm/v5,linux/arm/v6,linux/386,linux/arm64/v8,linux/ppc64le,linux/s390x

echo "Starting docker service"
systemctl start docker

echo "Setting up multi-arch build"
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
docker buildx rm builder
docker buildx create --name builder --driver docker-container --use
docker buildx inspect --bootstrap

docker buildx build --push --platform=$architectures -t cuupa/price-scraper:dev .
docker buildx build --push --platform=$architectures -t cuupa/price-scraper-amazon:dev ./scraper_modules/amazon
docker buildx build --push --platform=$architectures -t cuupa/price-scraper-amso:dev ./scraper_modules/amso
docker buildx build --push --platform=$architectures -t cuupa/price-scraper-minisforum:dev ./scraper_modules/minisforum
docker buildx build --push --platform=$architectures -t cuupa/price-scraper-yournextit:dev ./scraper_modules/yournextit

#sudo docker push cuupa/price-scraper -a
#sudo docker push cuupa/price-scraper-amazon -a
#sudo docker push cuupa/price-scraper-amso -a
#sudo docker push cuupa/price-scraper-minisforum -a
#sudo docker push cuupa/price-scraper-yournextit -a