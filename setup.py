from setuptools import setup, find_packages

#install_requires = ['vgl', 'pxlgrid'],
 
setup(name='libvgl',
    
    version='0.1',
    
    url='https://github.com/uhwang/vgl',
    
    license='None',
    
    author='Uisang Hwang',
    
    author_email='uhwangtx@gmail.com',
    
    description='Library Vector Graphic Library',
    
    install_requires=[
        "numpy",
        "moviepy",
        "pillow",
        "python-pptx",
        "pycairo",
        "pyquaternion",
        "PyQt5"
    ],
    
    classifiers      = ['Programming Language :: Python :: 3.x',
                        'Intended Audience :: Everybody',
                        'License :: None'
                        ]
    )
    #packages=find_packages(exclude=['tests']),
    
    #long_description=open('README.md').read(),
    
    #zip_safe=False,
    
    #setup_requires=['nose>=1.0'],
    
    #test_suite='nose.collector')