from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='email_notification',
    version='0.0.1',
    description='Simple package to send email when api fails.  ',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/BkrmDahal/email_notification',
    author='Bikram Dahal (Arch analytics)',
    author_email='bikram@archanalaytics.ai',
    license='MIT',
    python_requires='>=3',
    packages=[
        'email_notification'
    ],
    package_data={
        'hypermax': ['test'],
    },
    install_requires=[
        'PyYAML',
        'requests'
    ],
    classifiers=[
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
    ],
    platforms=['Linux', 'OS-X'],
    zip_safe=False
)