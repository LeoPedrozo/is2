import os
from contextlib import contextmanager
from fabric.api import cd, env, prefix, run, sudo, task

PROJECT_NAME = 'is2'
PROJECT_ROOT = '/var/www/%s' % PROJECT_NAME
VENV_DIR = os.path.join(PROJECT_ROOT, '.venv')
REPO = 'git@github.com:LeoPedrozo/%s.git' % PROJECT_NAME

env.hosts = []


@task
def staging():
    # env.hosts = ['luis@staging-server']
    env.hosts = ['luis@luis']
    env.environment = 'staging'


@task
def production():
    env.hosts = ['luis@production-server']
    env.environment = 'production'


# DO NOT EDIT ANYTHING BELOW THIS LINE!

@contextmanager
def source_virtualenv():
    with prefix('source ' + os.path.join(VENV_DIR, 'bin/activate')):
        yield


def clean():
    """Cleans Python bytecode"""
    sudo('find . -name \'*.py?\' -exec rm -rf {} \;')


def chown():
    """Sets proper permissions"""
    sudo('chown -R www-data:www-data %s' % PROJECT_ROOT)


def restart():
    sudo('supervisorctl reread')
    sudo('supervisorctl reload')
    sudo('service memcached restart')
    sudo('service nginx restart')


@task
def deploy():
    """
    Deploys the latest tag to the production server
    """
    sudo('chown -R %s:%s %s' % (env.user, env.user, PROJECT_ROOT))

    with cd(PROJECT_ROOT):
        run('git pull origin master')
        with source_virtualenv():
            with prefix('export DJANGO_SETTINGS_MODULE={}.settings.{}'.format(PROJECT_NAME, env.environment)):
                # run('source .env/bin/activate && pip install -r requirements/production.txt')
                run('source .env/bin/activate && pip install -r requirements.txt')
                run('./manage.py migrate')
                run('./manage.py collectstatic --noinput')

    chown()
    restart()


@task
def bootstrap():
    """Bootstrap the latest code at the app servers"""
    # sudo(
    #    'apt-get update && apt-get install git supervisor nginx memcached libjpeg8-dev postgresql libpq-dev python-dev python-pip python-virtualenv libfreetype6-dev libncurses5-dev'
    # )

    sudo('mkdir -p {}'.format(PROJECT_ROOT))
    sudo('chown -R {}:{} {}'.format(env.user, env.user, PROJECT_ROOT))
    run('git clone {} {}'.format(REPO, PROJECT_ROOT))

    with cd(PROJECT_ROOT):
        # run('git pull origin master')
        run('git pull origin iteracion_5')
        # run('virtualenv .env')
        run('python3 -m venv .venv')
        with source_virtualenv():
            # with prefix('export DJANGO_SETTINGS_MODULE={}.settings.{}'.format(PROJECT_NAME, env.environment)):
            with prefix('export DJANGO_SETTINGS_MODULE={}.settings'.format(PROJECT_NAME)):
                # run('source .env/bin/activate && pip install -r requirements/production.txt')
                run('source .venv/bin/activate && pip install -r requirements.txt')
                # run('./manage.py migrate')
                # run('./manage.py collectstatic --noinput')
                sudo('./manage.py collectstatic --noinput')

    chown()

    # Deploy web and app server configs
    for service in ('celerybeat', 'celerycam', 'celeryd', PROJECT_NAME):
        sudo('ln -s {project_root}/deploy/{environment}/{service}.conf /etc/supervisor/conf.d/{service}.conf'.format(
            project_root=PROJECT_ROOT, environment=env.environment, service=service))
    sudo('ln -s {project_root}/deploy/{environment}/nginx.conf /etc/nginx/sites-enabled/{project_name}.conf'.format(
        project_root=PROJECT_ROOT, environment=env.environment, project_name=PROJECT_NAME))

    restart()

    run('bash {project_root}/deploy/{environment}/restoreDB.sh'.format(project_root=PROJECT_ROOT,
                                                                       environment=env.environment))

    run('bash {project_root}/activarEntorno.sh'.format(project_root=PROJECT_ROOT))

