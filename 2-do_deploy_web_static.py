#!/usr/bin/python3
"""A Fabric script (based on the file 1-pack_web_static.py)"""

from fabric.api import run, env, put, sudo
from os.path import exists

env.hosts = ["107.23.58.213", "54.198.48.244"]


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
        folder_name = archive_filename.split('.')[0]
        target_folder = "/data/web_static/releases/{}".format(folder_name)
        run('mkdir -p {}'.format(target_folder))
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, target_folder))
        run('rm /tmp/{}'.format(archive_filename))
        run('sudo rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(target_folder))

        return True
    except Exception as e:
        return False
