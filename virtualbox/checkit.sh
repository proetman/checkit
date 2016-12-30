#!/bin/sh

echo "PEP8"
pep8 --max-line-length=120 $1 | more

echo "pylint"
pylint $1 | more
