#!/usr/bin/env python

import sys
import os.path
from Cython.Build import cythonize

try:
    from setuptools import setup, Extension
except ImportError:
    sys.stderr.write("Could not import 'setuptools', falling back to 'distutils'.\n")
    from distutils.core import setup, Extension

if (sys.version_info[0] < 3) or ((sys.version_info[0] == 3) and (sys.version_info[1] < 4)):
    sys.stderr.write("Error in setup script for HTSeq:\n")
    sys.stderr.write("Sorry, this version of HTSeq is for Python 3.4 or higher.\n")
    sys.exit(1)

try:
    import numpy
except ImportError:
    sys.stderr.write("Setup script for HTSeq: Failed to import 'numpy'.\n")
    sys.stderr.write("Please install numpy and then try again to install HTSeq.\n")
    sys.exit(1)

numpy_include_dir = os.path.join(os.path.dirname(numpy.__file__), 'core', 'include')


# Update version from VERSION file into module
with open('VERSION') as fversion:
    version = fversion.readline().rstrip()
with open('HTSeq/_version.py', 'wt') as fversion:
    fversion.write('__version__ = "'+version+'"')


setup(name='HTSeq',
      version=version,
      author='Simon Anders',
      author_email='sanders@fs.tum.de',
      maintainer='Fabio Zanini',
      maintainer_email='fabio.zanini@stanford.edu',
      url='http://www-huber.embl.de/users/anders/HTSeq/',
      description="A framework to process and analyze data from " +
                  "high-throughput sequencing (HTS) assays",
      classifiers=[
         'Development Status :: 5 - Production/Stable',
         'Topic :: Scientific/Engineering :: Bio-Informatics',
         'Intended Audience :: Developers',
         'Intended Audience :: Science/Research',
         'License :: OSI Approved :: GNU General Public License (GPL)',
         'Operating System :: POSIX',
         'Programming Language :: Python'
      ],
      requires=['numpy', 'python (>=3.4)'],
      py_modules=[
         'HTSeq._HTSeq_internal',
         'HTSeq.StepVector',
         'HTSeq._version',
         'HTSeq.scripts.qa',
         'HTSeq.scripts.count'
      ],
      ext_modules=cythonize(
             module_list=['src/HTSeq/_HTSeq.pyx'],
             working='src',
             include_dirs=[numpy_include_dir],
             extra_compile_args=['-w'],
      ) + [
         #Extension(
         #    'HTSeq._HTSeq',
         #    ['src/_HTSeq.c'],
         #    include_dirs=[numpy_include_dir],
         #    extra_compile_args=['-w']),
         Extension(
             'HTSeq._StepVector',
             ['src/StepVector_wrap.cxx'],
             extra_compile_args=['-w']),
      ],
      scripts=[
         'scripts/htseq-qa',
         'scripts/htseq-count',
      ]
      )
