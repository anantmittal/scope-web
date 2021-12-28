"""
Tasks for ensuring project dependencies are installed.
"""

from aws_infrastructure.tasks import compose_collection
import aws_infrastructure.tasks.library.dependencies
from invoke import Collection


CONFIG_KEY = 'dependencies'
DEPENDENCIES = {
    'all': aws_infrastructure.tasks.library.dependencies.Dependency(
        pipfile_dirs=[
            '.',
            './server_celery',
            './server_flask',
        ],
        yarn_dirs=[
            './web_registry',
        ]
    ),
    'python': aws_infrastructure.tasks.library.dependencies.Dependency(
        pipfile_dirs=[
            '.',
            './server_celery',
            './server_flask',
        ],
        yarn_dirs=None,
    ),
    'root': aws_infrastructure.tasks.library.dependencies.Dependency(
        pipfile_dirs=['.'],
        yarn_dirs=None
    ),
    'celery': aws_infrastructure.tasks.library.dependencies.Dependency(
        pipfile_dirs=['./server_celery'],
        yarn_dirs=None
    ),
    'flask': aws_infrastructure.tasks.library.dependencies.Dependency(
        pipfile_dirs=['./server_flask'],
        yarn_dirs=None
    ),
    'registry': aws_infrastructure.tasks.library.dependencies.Dependency(
        pipfile_dirs=None,
        yarn_dirs=['./web_registry']
    ),
}


ns = Collection('dependencies')

ns_dependencies = aws_infrastructure.tasks.library.dependencies.create_tasks(
    config_key=CONFIG_KEY,
    dependencies=DEPENDENCIES,
)

compose_collection(
    ns,
    ns_dependencies,
    sub=False,
)
