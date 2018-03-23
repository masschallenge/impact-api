docker run --rm  -v"$(pwd)":/app  -ti semantic-release  -- semantic-release version
export pwd=$(pwd)
export TAG=$(docker run --tty=false --rm  -v$pwd:/app  -i semantic-release -- semantic-release version --noop | grep "Current version: " | cut -d ' ' -f 3 | sed -e "s/\r//")
echo $TAG
git push
git push --tags
cd ../django-accelerator && git tag "v${TAG}"
git push --tags 
cd ../accelerate && git tag "v${TAG}"
git push --tags