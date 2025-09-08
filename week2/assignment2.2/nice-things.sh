#!/bin/sh

NAME="$1"

if [ -z "$NAME" ]; then
    echo "Usage: $0 <name>"
    exit 1
fi

echo "$NAME is thoughtful."
echo "$NAME has a great sense of humor."
echo "$NAME makes people feel welcome."