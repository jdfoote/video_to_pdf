import re
import os
import subprocess
import shutil
import argparse


parser = argparse.ArgumentParser(description='Change an mp4 file to a PDF')
parser.add_argument('-i', help='Location of the mp4 file')
parser.add_argument('-p', type=int, help='Number of pages to output', default = None)
parser.add_argument('-o', type=str, help='Output file location')

args = parser.parse_args()

video_fn = args.i
pdf_fn = args.o
page_count = args.p

os.mkdir('tmp')

try:
    subprocess.run(['python', './video_to_ascii/cli.py',
        '-f', video_fn,
        '--strategy', 'reverse-ascii',
        '-o', './tmp/tmp.sh'])
except Exception:
    print('Make sure video-to-ascii is installed (pip install video-to-ascii)')


output = []
with open('tmp/tmp.sh', 'r') as infile:
    curr_page = ''
    next(infile) # Skip bash header
    for line in infile:
        if page_count and len(output) > page_count:
            break
        if re.match("sleep", line) or re.match(r"echo -en '.\[", line):
            if curr_page != '':
                output.append(curr_page)
            curr_page = ''
            continue
        else:
            line = re.sub("echo -en '",'',line)
            line = re.sub("[\r']",'',line)
            curr_line = ''
            if len(line) < 10:
                continue
            for char in line:
                try:
                    char.encode('latin-1')
                    curr_line += char
                except:
                    print('bad character: {}'.format(char))
                    continue
            curr_page = curr_page + line
    if curr_page != '':
        output.append(curr_page)

with open('tmp/tmp.tex', 'w') as f:
    f.write('''\\documentclass[8pt]{article}
\\usepackage{listings}
\\lstset{basicstyle=\\tiny,
    stringstyle=\\ttfamily}
\\usepackage[a4paper, margin=.6in, landscape]{geometry}
\\usepackage{setspace}
\\setstretch{1.4}
\\begin{document}
\\setlength\\parindent{0pt}\n''')
    for page in output:
        f.write('\\begin{lstlisting}\n')
        f.write(page)
        f.write('\\end{lstlisting}')
        f.write('\n\\pagebreak\n')
    f.write('\\end{document}')

try:
    subprocess.run(['pdflatex', '-output-directory', 'tmp',
        'tmp/tmp.tex'])
except Exception:
    print('Make sure that pdflatex is installed')

os.rename('tmp/tmp.pdf', pdf_fn)

shutil.rmtree('./tmp/')
