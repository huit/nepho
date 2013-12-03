#!/usr/bin/env python
# https://coderwall.com/p/qawuyq
#
import os
import pypandoc

markdown = 'README.md'
rst = 'README.rst'

converted = pypandoc.convert(markdown, 'rst')
f = open(rst, 'w+')
f.write(converted)
f.close()
os.system('python setup.py register sdist bdist_egg upload')
os.remove(rst)
