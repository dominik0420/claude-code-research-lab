#!/usr/bin/env python3
# Thin wrapper — actual logic in lab/scripts/compile_paper.py
import os, sys, runpy
here   = os.path.dirname(os.path.abspath(__file__))
target = os.path.normpath(os.path.join(here, chr(46)+chr(46), chr(46)+chr(46), "lab", "scripts", "compile_paper.py"))
sys.argv[0] = target
runpy.run_path(target, run_name="__main__")
