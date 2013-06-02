try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="shell",
    version="1.0.0",
    description="A better way to run shell commands in Python.",
    author='Daniel Lindsley',
    author_email='daniel@toastdriven.com',
    long_description=open('README.rst', 'r').read(),
    py_modules=[
        'shell'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: System :: Shells',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    url='http://github.com/toastdriven/shell',
    license='BSD'
)
