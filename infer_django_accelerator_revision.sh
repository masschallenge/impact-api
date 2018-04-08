#!/bin/bash
DEFAULT_BRANCH=development

# allow for an override, if DJANGO_ACCELERATOR_REVISION is already set in env.
if ! [[ -z $DJANGO_ACCELERATOR_REVISION ]];then
  echo $DJANGO_ACCELERATOR_REVISION
  exit
fi

# use default branch if input parameter is missing
if [[ -z $1 ]]; then
  REQUESTED_REVISION=$DEFAULT_BRANCH
else
  REQUESTED_REVISION=$1
fi

# check if the requested revision exists in remote
PARSED_REVISION=`git ls-remote https://www.github.com/masschallenge/django-accelerator.git $REQUESTED_REVISION | xargs echo | tr -s ' ' | cut -d ' ' -f 2 | cut -d'/' -f 3`

# Use DEFAULT_BRANCH if PARSED_REVISION is empty
if [[ -z $PARSED_REVISION ]]; then
  # check if exists as commit sha1
  mkdir django-accelerator
  cd django-accelerator
  git init -q
  git remote add origin https://github.com/masschallenge/django-accelerator.git
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
  rm -rf django-accelerator/
else
  INFERRED_REVISION=$PARSED_REVISION
fi

# Return the inferred revision
export DJANGO_ACCELERATOR_REVISION=$INFERRED_REVISION
echo $INFERRED_REVISION
exit