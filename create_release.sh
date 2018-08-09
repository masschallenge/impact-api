
# if a tag hasn't been passed in as a parameter, create a semantic one
if [ ! -n "$TAG" ]; then
    git commit --allow-empty -m "generating a new release"
	git push
    docker run --rm  -v"$(pwd)":/app  -ti semantic-release  -- semantic-release version
    export pwd=$(pwd)
    export TAG=$(docker run --tty=false --rm  -v$pwd:/app  -i semantic-release -- semantic-release version --noop | grep "Current version: " | cut -d ' ' -f 3 | sed -e "s/\r//")
else
    echo "You passed in '$TAG' as the custom tag"
    # TR == test release
    echo "We're going to refactor the tag into 'TR-$TAG' to avoid any conflicts."
    TAG="TR-$TAG"
fi

echo $TAG

git push
git push --tags
cd ../django-accelerator && git tag "v${TAG}"
git push --tags 
cd ../accelerate && git tag "v${TAG}"
git push --tags
cd ../directory && git tag "v${TAG}"
git push --tags