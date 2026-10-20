#!/bin/sh
# SPDX-License-Identifier: MIT
# Per-process global lock. Do not wrap a complete lifecycle in flock.
exec flock /tmp/lowpoly-production-blender.lock /usr/bin/blender "$@"
