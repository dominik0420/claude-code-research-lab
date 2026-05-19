#!/usr/bin/env python3
# Thin wrapper 鈥?actual logic lives in lab/scripts/export_survey.py
import os, sys, runpy
here   = os.path.dirname(os.path.abspath(__file__))
target = os.path.normpath(os.path.join(here, '..', '..', 'lab', 'scripts', 'export_survey.py'))
sys.argv[0] = target
runpy.run_path(target, run_name='__main__')
