from setuptools import setup

setup(name='guac',
    version='1.0.0',
    description='Monadic do-notation in Python',
    url='https://github.com/JadenGeller/Guac',
    author='Jaden Geller',
    license='MIT',
    packages=['guac'],
    classifiers=['Intended Audience :: Developers',
                 'Intended Audience :: Education'
                 'Topic :: Software Development :: Libraries',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3 :: Only',
                 'Programming Language :: Python :: Implementation :: PyPy'
                 ],
    keywords='monad monadic coroutine generator pypy backtracking',
    zip_safe=True)
