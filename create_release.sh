
# if a tag hasn't been passed in as a parameter, create a semantic one
if [ ! -n "$tag" ]; then
    git commit --allow-empty -m "generating a new release"
    docker run --rm  -v"$(pwd)":/app  -ti semantic-release  -- semantic-release version
    export pwd=$(pwd)
    git push        
    export TAG=$(docker run --tty=false --rm  -v$pwd:/app  -i semantic-release -- semantic-release version --noop | grep "Current version: " | cut -d ' ' -f 3 | sed -e "s/\r//")
else
    echo "You passed in '$tag' as the custom tag"
    # TR == test release
    echo "Renaming as 'TR-$tag' to avoid potential conflicts."
    export TAG="TR-$tag"
fi

echo $TAG

git tag "v${TAG}"
git push --tags
cd ../django-accelerator && git tag "v${TAG}"
git push --tags 
cd ../accelerate && git tag "v${TAG}"
git push --tags
cd ../front-end && git tag "v${TAG}"
git push --tags
cd ../semantic-ui-theme && git tag "v${TAG}"
git push --tags
