# Overview

This project is the first in a suite of tools designed for [Exceedingly Reproducibly Research](https://blog.communitydata.cc/exceedingly-reproducible-research/) by the [Community Data Science Collective](http://communitydata.cc). The goal of this project is to convert pdf representations of lab meetings and other conversations, which can be annotated with audio and timestamps.

# Usage

Using this script requires the following dependencies:

- Python 3.5+
- pdflatex

The script takes three parameters: an input file, and output file, and the number of pages to produce.

E.g.,

python3 video_to_pdf.py -i path/to/input/file.mp4 -o path/to/output/file.pdf -p 100


# Acknowledgements

The projet extensively uses the [video_to_ascii](https://github.com/joelibaceta/video-to-ascii) project.
