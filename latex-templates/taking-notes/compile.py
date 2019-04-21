#!/usr/bin/python
import subprocess, sys

commands = [
    ['pdflatex', '-shell-escape' , sys.argv[1] + '.tex'],
    ['biber', sys.argv[1] + '.bcf'], 
    ['pdflatex', '-shell-escape' , sys.argv[1] + '.tex'],
]

for c in commands:
    subprocess.call(c)
