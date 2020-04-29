
# if a tag hasn't been passed in as a parameter, create a semantic one
if [ ! -n "$tag" ]; then
    git commit --allow-empty -m "generating a new release"
    docker run --rm  -v"$(pwd)":/app  -ti semantic-release  -- semantic-release version
    export pwd=$(pwd)
    git push        
    export TAG=$(docker run --tty=false --rm  -v$pwd:/app  -i semantic-release -- semantic-release version --noop | grep "Current version: " | cut -d ' ' -f 3 | sed -e "s/\r//")
else
    echo "You passed in '$tag' as the custom tag"
    echo "Renaming as 'TR-$tag' (Test Release) to avoid potential conflicts."
    export TAG="TR-$tag"
fi

export VTAG="v{$TAG}"
echo $VTAG


# Tag all four repos and push tags to origin

git tag $VTAG
git push --tags

cd ../django-accelerator && git tag $VTAG && git push --tags
cd ../front-end && git tag $VTAG && git push --tags

# In accelerate, we also update the impact-api submodule version
cd ../accelerate
cd mcproject/api/
# impact-api $VTAG was pushed above; fetch, checkout, and update .gitmodules
git fetch && git checkout $VTAG
cd ../..
git add .gitmodules && git commit -m "Updated submodule to $VTAG"
git tag $VTAG
git push --tags
