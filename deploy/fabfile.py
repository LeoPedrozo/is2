import os
import sys
from contextlib import contextmanager
from fabric.api import cd, env, prefix, run, sudo, task


def menuTag():
    print("""
    Ingrese una opción: 
    1. Tag v0.1
    2. Tag v0.2
    3. Tag v0.3
    4. Tag v0.4
    5. Tag v0.5""")

    return "v0." + input() + "-alpha"


def menuEjecucion():
    retorno = "desarrollo"
    if TAG == "v0.5-alpha":
        print("""
        Ingrese una opción: 
        1. Ejecutar en modo desarrollo
        2. Ejecutar en modo Produccion""")
        if (int(input()) == 1):
            retorno = "desarrollo"
        else:
            retorno = "produccion"
    else:
        print("""
        Ingrese una opción: 
        1. Ejecutar en modo desarrollo
        """)
        if (int(input()) == 1):
            retorno = "desarrollo"
    return retorno


def limpiarDeploy():
    """Limpia el directorio de despliegue"""
    # check if the directory exists
    if os.path.exists(PROJECT_ROOT):
        sudo('rm -rf %s' % PROJECT_ROOT)
        sudo('rm /etc/supervisor/conf.d/celeryd.conf || true')
        sudo('rm /etc/supervisor/conf.d/celerycam.conf || true')
        sudo('rm /etc/supervisor/conf.d/celerybeat.conf || true')
        sudo('rm /etc/supervisor/conf.d/{}.conf || true'.format(PROJECT_NAME))
        sudo('rm /etc/nginx/sites-enabled/{}.conf || true'.format(PROJECT_NAME))


env.password = 'luis'
PROJECT_NAME = 'is2'
PROJECT_ROOT = '/var/www/%s' % PROJECT_NAME
VENV_DIR = os.path.join(PROJECT_ROOT, '.venv')
REPO = 'git@github.com:LeoPedrozo/%s.git' % PROJECT_NAME
SITE_ID = '7'

TAG = menuTag()

ENTORNO = menuEjecucion()

env.hosts = []


@task
def staging():
    # env.hosts = ['luis@staging-server']
    env.hosts = ['luis@luis']
    env.environment = 'staging'


@task
def production():
    # env.hosts = ['luis@production-server']
    env.hosts = ['luis@luis']
    env.environment = 'staging'
    # env.environment = 'production'


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
    limpiarDeploy()
    """Bootstrap the latest code at the app servers"""
    # sudo(
    #    'apt-get update && apt-get install git supervisor nginx memcached libjpeg8-dev postgresql libpq-dev python-dev python-pip python-virtualenv libfreetype6-dev libncurses5-dev'
    # )

    sudo('mkdir -p {}'.format(PROJECT_ROOT))
    sudo('chown -R {}:{} {}'.format(env.user, env.user, PROJECT_ROOT))
    run('git clone -b {} --single-branch {} {}'.format(TAG, REPO, PROJECT_ROOT))

    with cd(PROJECT_ROOT):
        # run('git pull origin master')
        # run('git pull origin iteracion_5')
        # run('virtualenv .env')
        run('python3 -m venv .venv')
        with source_virtualenv():
            # with prefix('export DJANGO_SETTINGS_MODULE={}.settings.{}'.format(PROJECT_NAME, env.environment)):
            with prefix('export DJANGO_SETTINGS_MODULE={}.settings'.format(PROJECT_NAME)):
                # run('source .env/bin/activate && pip install -r requirements/production.txt')
                run('source .venv/bin/activate && pip install wheel && pip install -r requirements.txt')
                # run('./manage.py migrate')
                # run('./manage.py collectstatic --noinput')
                sudo('./manage.py collectstatic --noinput')

    chown()

    if ENTORNO == "produccion":
        # Deploy web and app server configs
        # Si la iteracion lleva dentro las configuraciones de produccion
        for service in ('celerybeat', 'celerycam', 'celeryd', PROJECT_NAME):
            sudo(
                'ln -s {project_root}/deploy/{environment}/{service}.conf /etc/supervisor/conf.d/{service}.conf'.format(
                    project_root=PROJECT_ROOT, environment=env.environment, service=service))

        sudo('ln -s {project_root}/deploy/{environment}/nginx.conf /etc/nginx/sites-enabled/{project_name}.conf'.format(
            project_root=PROJECT_ROOT, environment=env.environment, project_name=PROJECT_NAME))
        # sino

        restart()

    # restaurar base de datos
    if TAG == "v0.5-alpha":
        run('bash {project_root}/deploy/{environment}/restoreDB.sh'.format(project_root=PROJECT_ROOT,
                                                                           environment=env.environment))
        run('bash {project_root}/activarEntorno.sh'.format(project_root=PROJECT_ROOT))

    sudo('chmod -R 777 {project_root}/'.format(project_root=PROJECT_ROOT))

    # Para borrar las migraciones
    run('find {project_root} -path "*/migrations/*.py" -not -name "__init__.py" -delete'.format(
        project_root=PROJECT_ROOT))
    run('find {project_root} -path "*/migrations/*.pyc"  -delete'.format(project_root=PROJECT_ROOT))

    # arreglar dependencias de django

    with cd(PROJECT_ROOT):
        with source_virtualenv():
            run('pip uninstall -y django')
            run('pip install django==3.2.6')

            # make django migrations
            run('./manage.py makemigrations')
            # fake migrate
            run('./manage.py migrate --fake')

    run("sed -i '/SITE_ID*/c\SITE_ID = {site_id}' {project_root}/{project_name}/settings.py".format(site_id=SITE_ID,
                                                                                                    project_root=PROJECT_ROOT,
                                                                                                    project_name=PROJECT_NAME))

    # si el servidor es desarrollo
    if ENTORNO == "desarrollo":
        sys.exit(0)
    else:
        sys.exit(1)
