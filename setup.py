from setuptools import setup

kwargs = {
    'name': 'abaqus-to-exodus',
    'version': '0.0.1',
    'packages': ['groups_to_blocks'],
    'entry_points': {
        'console_scripts': [
            'groups-to-blocks=groups_to_blocks.__main__:main'
        ]
    },

    # Metadata
    'author': 'Matthew Nyberg',
    'author_email': 'mnyberg@wisc.edu',
    'description': 'Tool to convert Abaqus meshes to an Exodus format ready for transport in OpenMC',
    'url': 'https://github.com/NybergWISC/abaqus_cubit_exodus',
    'download_url': 'https://github.com/NybergWISC/abaqus_cubit_exodus',
    'project_urls': {
        'Issue Tracker': 'https://github.com/NybergWISC/abaqus_cubit_exodus/issues',
        'Source Code': 'https://github.com/NybergWISC/abaqus_cubit_exodus',
    },
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
}

setup(**kwargs)