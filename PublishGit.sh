#!/bin/env bash
git pull
git add .
git commit -m "$*"
git push
