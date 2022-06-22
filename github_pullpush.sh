#!/bin/bash

cd "$(dirname "$0")"

echo -e "\n### GIT ADD"
git add --all --verbose
echo -e "\n### GIT STATUS"
git status
echo -e "\n### GIT COMMIT"
git commit -m "Commit $(date '+%Y-%m-%d %H:%M:%S')"
echo -e "\n### GIT PULL"
git pull
echo -e "\n### GIT PUSH"
git push

