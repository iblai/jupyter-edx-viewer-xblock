"""Setup for xblocktimetracker XBlock."""

import os
from setuptools import setup


def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='xblock_jupyter_viewer',
    version='1.0.1',
    description='View Jupyter Notebooks in your XBlock',
    license='UNKNOWN',          # TODO: choose a license: 'AGPL v3' and 'Apache 2.0' are popular.
    packages=[
        'xblock_jupyter_viewer',
    ],
    install_requires=[
        'XBlock',
        'nbconvert',
        'nbformat',
        'requests'
    ],
    entry_points={
        'xblock.v1': [
            'xblock_jupyter_viewer = xblock_jupyter_viewer:JupyterViewerXBlock',
        ]
    },
    package_data=package_data("xblock_jupyter_viewer", ["static", "public", "rest"]),
)
