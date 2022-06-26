from setuptools import setup

VERSION = '0.0.2' 
DESCRIPTION = 'Python layout tool for photonic integrated circuits.'
LONG_DESCRIPTION = 'Python layout tool for photonic integrated circuits.'

# Setting up
setup(
       # the name must match the folder name 'palgds'
        name="palgds", 
        version=VERSION,
        author="Kazim Gorgulu",
        author_email="<youremail@email.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=["palgds"],
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)