#!/bin/sh
exec flock /tmp/lowpoly-production-blender.lock /usr/bin/blender "$@"
