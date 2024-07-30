#!/usr/bin/env python
import glob
import sys
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

# Collect sources
c_sources = glob.glob('crfsuite/lib/crf/src/*.c') + ['crfsuite/lib/cqdb/src/cqdb.c', 'crfsuite/lib/cqdb/src/lookup3.c']
cpp_sources = ['pycrfsuite/_pycrfsuite.cpp', 'pycrfsuite/trainer_wrapper.cpp'] + glob.glob('crfsuite/swig/*.cpp')
lbfgs_sources = glob.glob('liblbfgs/lib/*.c')

includes = [
    'crfsuite/include/',
    'crfsuite/lib/cqdb/include',
    'liblbfgs/include',
    'pycrfsuite',
]

class build_ext_check_gcc(build_ext):
    def build_extensions(self):
        c = self.compiler

        _compile = c._compile

        def c_compile(obj, src, ext, cc_args, extra_postargs, pp_opts):
            if src.endswith('.c'):
                cc_args = cc_args + ['-std=c99']
            return _compile(obj, src, ext, cc_args, extra_postargs, pp_opts)

        def cpp_compile(obj, src, ext, cc_args, extra_postargs, pp_opts):
            if src.endswith('.cpp'):
                extra_postargs = extra_postargs + ['-std=c++11']
            return _compile(obj, src, ext, cc_args, extra_postargs, pp_opts)

        if c.compiler_type == 'unix':
            c._compile = c_compile
            c._c_compile = c_compile
            c._cpp_compile = cpp_compile

        elif c.compiler_type == "msvc":
            if sys.version_info[:2] < (3, 5):
                c.include_dirs.extend(['crfsuite/win32'])

        build_ext.build_extensions(self)

ext_modules = [
    Extension('pycrfsuite._pycrfsuite',
        include_dirs=includes,
        language='c++',
        sources=cpp_sources + lbfgs_sources
    ),
    Extension('pycrfsuite._pycrfsuite_c',
        include_dirs=includes,
        language='c',
        sources=c_sources
    ),
]

setup(
    name='python-crfsuite',
    version="0.9.10",
    description="Python binding for CRFsuite",
    long_description=open('README.rst').read(),
    author="Terry Peng, Mikhail Korobov",
    author_email="pengtaoo@gmail.com, kmike84@gmail.com",
    license="MIT",
    url='https://github.com/scrapinghub/python-crfsuite',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Cython",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Text Processing :: Linguistic",
    ],
    zip_safe=False,
    packages=['pycrfsuite'],
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext_check_gcc},
)
