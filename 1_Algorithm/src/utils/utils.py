import os


def read_file(filePath):
    return "123"

def get_project_path():
    """得到项目路径"""
    project_path = os.path.join(
        os.path.dirname(__file__)
    )
    return project_path