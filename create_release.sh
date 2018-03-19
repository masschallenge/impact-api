semantic-release --major version
export TAG=$(semantic-release version --noop | grep "Current version: " | cut -d ' ' -f 3)
cd ../django-accelerator && git tag $TAG && git push --tags 
cd ../accelerate && git tag $TAG && git push --tags