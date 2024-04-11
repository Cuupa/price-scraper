app_version=0.8

amazon_scraper_version=0.3
amso_scraper_version=0.3
minisforum_scraper_version=0.4
yournextit_scraper_version=0.3

architectures=linux/amd64,linux/arm64,linux/arm/v7,linux/arm/v5,linux/arm/v6,linux/386,linux/arm64/v8,linux/ppc64le,linux/s390x

echo "Starting docker service"
systemctl start docker

echo "Setting up multi-arch build"
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
docker buildx rm builder
docker buildx create --name builder --driver docker-container --use
docker buildx inspect --bootstrap

echo "BUILDING APP IN VERSION $app_version"
docker buildx build --push --platform=$architectures -t cuupa/price-scraper:$app_version .
docker buildx build --push --platform=$architectures -t cuupa/price-scraper:latest .

echo "BUILDING AMAZON-SCRAPER IN VERSION $amazon_scraper_version"
docker buildx build --push --platform=$architectures -t cuupa/price-scraper-amazon:$amazon_scraper_version ./scraper_modules/amazon
docker buildx build --push --platform=$architectures -t cuupa/price-scraper-amazon:latest ./scraper_modules/amazon

echo "BUILDING AMSO-SCRAPER IN VERSION $amso_scraper_version"
docker buildx build --push --platform=$architectures -t cuupa/price-scraper-amso:$amso_scraper_version ./scraper_modules/amso
docker buildx build --push --platform=$architectures -t cuupa/price-scraper-amso:latest ./scraper_modules/amso

echo "BUILDING MINISFORUM-SCRAPER IN VERSION $minisforum_scraper_version"
docker buildx build --push --platform=$architectures -t cuupa/price-scraper-minisforum:$minisforum_scraper_version ./scraper_modules/minisforum
docker buildx build --push --platform=$architectures -t cuupa/price-scraper-minisforum:latest ./scraper_modules/minisforum

echo "BUILDING YOURNEXTIT-SCRAPER IN VERSION $yournextit_scraper_version"
docker buildx build --push --platform=$architectures -t cuupa/price-scraper-yournextit:$yournextit_scraper_version ./scraper_modules/yournextit
docker buildx build --push --platform=$architectures -t cuupa/price-scraper-yournextit:latest ./scraper_modules/yournextit

#sudo docker push cuupa/price-scraper -a
#sudo docker push cuupa/price-scraper-amazon -a
#sudo docker push cuupa/price-scraper-amso -a
#sudo docker push cuupa/price-scraper-minisforum -a
#sudo docker push cuupa/price-scraper-yournextit -a