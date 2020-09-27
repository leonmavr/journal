#!/usr/bin/python
import os
import subprocess, sys
import glob


def cleanup():
    exts = ['*.log', '*.bcf', '*.run.xml', '*.toc', '*.aux', '*.out', '*.bbl',
            '*.blg', '_minted-main']
    to_remove = [glob.glob(e)[0] for e in exts if len(glob.glob(e)) != 0]
    cmd = ['rm', '-rf', *to_remove]
    subprocess.call(cmd)


def compile(fname = 'main.tex'):
    fname_no_ext = fname.split('.')[0]
    commands = [
        ['pdflatex', '--shell-escape' , fname_no_ext + '.tex'],
        ['biber', fname_no_ext + '.bcf'], 
        ['pdflatex', '--shell-escape' , fname_no_ext + '.tex'],
    ]
    for c in commands:
        subprocess.call(c)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        compile()
    else:
        assert os.path.isfile(sys.argv[1]), "Please provide a .tex file to compile"
        compile(sys.argv[1])
    cleanup()
