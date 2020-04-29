# If a tag hasn't been passed in as a parameter, create a semantic one
if [ ! -n "$tag" ]; then
    git commit --allow-empty -m "Generating a new release"
    docker run --rm  -v"$(pwd)":/app  -ti semantic-release  -- semantic-release version
    export pwd=$(pwd)
    git push
    export TAG=$(docker run --tty=false --rm  -v$pwd:/app  -i semantic-release -- semantic-release version --noop | grep "Current version: " | cut -d ' ' -f 3 | sed -e "s/\r//")
else
    echo "You passed in '$tag' as the custom tag"
    echo "Tagging as 'vTR-$tag' (Test Release) to avoid potential conflicts."
    export TAG="TR-$tag"
fi
export VTAG="v$TAG"


# Tag all four repos and push tags to origin

echo "Tagging impact-api as $VTAG"
git tag $VTAG && git push --tags
echo "Tagging django-accelerator as $VTAG"
cd ../django-accelerator && git tag $VTAG && git push --tags
echo "Tagging front-end as $VTAG"
cd ../front-end && git tag $VTAG && git push --tags

# In accelerate, we also update the impact-api submodule version
echo "Tagging accelerate as $VTAG"
cd ../accelerate/mcproject/api/
# impact-api $VTAG was pushed above; fetch, checkout, and update .gitmodules
echo "Updating impact-api submodule to $VTAG"
git fetch && git checkout $VTAG
cd ../..
git add .gitmodules && git commit -m "Updated submodule to $VTAG"
git tag $VTAG && git push --tags
