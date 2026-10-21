# SPDX-License-Identifier: MIT
"""Run the two independent measurement routines in one blocking Blender process."""
import pathlib,runpy
P=pathlib.Path(__file__).resolve().parent
runpy.run_path(str(P/'measure-geometry.py'),run_name='__main__')
runpy.run_path(str(P/'measure-hierarchy.py'),run_name='__main__')
