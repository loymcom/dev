#! /bin/bash

repo=../OCA/calendar
module=resource_booking
user_org=ows-cloud


cd $repo
# git add --all
# git commit -m "[MIG] $module: Migration to 16.0"
git remote add $user_org git@github.com:$user_org/$repo.git # This mode requires an SSH key in the GitHub account
git push $user_org 16.0-mig-$module --set-upstream