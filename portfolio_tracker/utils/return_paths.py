"""
Created on: 14 Dec 2023
Utility functions to return useful paths
"""

import os


def get_project_dir() -> str:
    """
    Retrieve the path of the project directory, going up two levels in the folder structure.

    Returns:
        str: The absolute path of the project directory.
    """
    current_dir = os.getcwd()
    project_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
    return project_dir
