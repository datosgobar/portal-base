#!/usr/bin/env bash

set -ev

branch="$BRANCH_TO_USE"
pattern="^[0-9.]+"

if [ "$branch" == "master" ]; then
    tag="latest"
elif [[ "$branch" =~ $pattern ]]; then
    tag="release-$branch"
else
    tag="$branch"
fi

echo Using branch: "$branch", and tag: "$tag"
image="datosgobar/portal-base:build"
image_full_name="datosgobar/portal-base:$tag"
docker login -u="$DOCKER_USERNAME" -p="$DOCKER_PASS";
docker tag "$image" "$image_full_name"
echo "Deploying image $image_full_name"
docker push "$image_full_name"
echo "Deploy finished!"
exit 0