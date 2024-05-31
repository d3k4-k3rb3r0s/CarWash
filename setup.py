from setuptools import setup, find_packages

setup(
    name='CarWash',
    version='1.0.4',
    description='Research/RedTeamers tool to automate the Wash>Reaver(pixiedust)>* workflow with cyberpunk themed output.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='d3k4t3ss3r4',
    url='https://github.com/d3k4-k3rb3r0s/CarWash',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'CarWash=CarWash:carwash',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.6',
)
