#!/bin/bash
DEFAULT_BRANCH=development

REVISION_ARG=$1
REPO_URL=$2

# allow for an override, if DJANGO_ACCELERATOR_REVISION is already set in env.
if [[  (! -z $DJANGO_ACCELERATOR_REVISION) && $REPO_URL == *"django-accelerator"* ]];then
  echo $DJANGO_ACCELERATOR_REVISION
  exit
fi
# allow for an override, if DIRECTORY_REVISION is already set in env.
if ! [[ (! -z $DIRECTORY_REVISION) && $REPO_URL == *"directory"* ]];then
  echo $DIRECTORY_REVISION
  exit
fi

# use default branch if input parameter is missing
if [[ -z $REVISION_ARG ]]; then
  REQUESTED_REVISION=$DEFAULT_BRANCH
else
  REQUESTED_REVISION=$REVISION_ARG
fi

# check if the requested revision exists in remote
PARSED_REVISION=`git ls-remote $REPO_URL $REQUESTED_REVISION | xargs echo | tr -s ' ' | cut -d ' ' -f 2 | cut -d'/' -f 3`

# Use DEFAULT_BRANCH if PARSED_REVISION is empty
if [[ -z $PARSED_REVISION ]]; then
  # check if exists as commit sha1
  mkdir tmp-repo-dir
  cd tmp-repo-dir
  git init -q
  git remote add origin $REPO_URL
  git fetch origin -qt --dry-run  # does not get files, but updates commit info
  REVISION_VALID_IF_EMPTY=`git cat-file -e $REQUESTED_REVISION 2>&1`
  # if variable is empty, then this is a valid revision, use it.
  if [[ -z $REVISION_VALID_IF_EMPTY ]]; then
    INFERRED_REVISION=$REQUESTED_REVISION
  else
    # not a valid branch, tag or revision. Use default branch.
    INFERRED_REVISION=$DEFAULT_BRANCH
  fi
  # clean up the directory
  cd ..
  rm -rf tmp-repo-dir/
else
  INFERRED_REVISION=$PARSED_REVISION
fi

# Return the inferred revision
echo $INFERRED_REVISION
exit