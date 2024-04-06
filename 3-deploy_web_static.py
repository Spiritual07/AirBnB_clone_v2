#!/usr/bin/python3
from fabric.api import local, run, env, put, sudo
from time import strftime
from datetime import date
from os.path import exists

env.hosts = ["107.23.58.213", "54.198.48.244"]


def do_pack():
    """ A script that generates archive the contents of web_static folder"""

    filename = strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -czvf versions/web_static_{}.tgz web_static/"
              .format(filename))

        return "versions/web_static_{}.tgz".format(filename)

    except Exception as e:
        return None


def do_deploy(archive_path):
    """
    A Fabric script that distributes an archive to your web servers,
    using the function do_deploy
    """

    if not exists(archive_path):
        return False
    try:
        # Upload the archive to /tmp/ directory on the web server
        put(archive_path, '/tmp/')

        # Extract archive to /data/web_static/releases/
        # <archive filename without extension>
        archive_filename = archive_path.split('/')[-1]
        filename = archive_filename.split('.')[0]
        target_folder = "/data/web_static/releases/{}".format(filename)
        run('mkdir -p {}'.format(target_folder))
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, target_folder))
        run('rm /tmp/{}'.format(archive_filename))
        run("mv /data/web_static/releases/{}/web_static/*\
            /data/web_static/releases/{}/".format(filename, filename))
        run("rm -rf /data/web_static/releases/{}/web_static".format(filename))
        run('sudo rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(target_folder))

        return True
    except Exception as e:
        return False


def deploy():
    """
    A Fabric script that creates and distributes an archive to your web
    servers, using the function deploy
    """

    path = do_pack()

    if not path:
        return False

    return do_deploy(path)
