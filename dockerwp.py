#!/usr/bin/python2

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from cement.core import handler
import subprocess
import os
import platform
import sqlite3
conn = sqlite3.connect('example.db')


class MyBaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = "Docker WP CLI. (c) 2015 Etopian Inc."
        arguments = [
            ( ['-f', '--foo'],
              dict(action='store', help='the notorious foo option') ),
            ( ['-d', '--domain'],
              dict(action='store', help='The domain name for instance site.com, exclude www.') ),
            ( ['-s', '--sub_domain'],
              dict(action='store', help='Specify a subdomain, like www.') ),
            ( ['-C'],
              dict(action='store_true', help='the big C option') ),
            ]



    def version(self):
        release = open("/etc/os-release")

    @expose(hide=True)
    def default(self):
        self.app.log.info('Docker WordPress CLI. Type dockerwp --help for more information.')
        if self.app.pargs.foo:
            print("Recieved option: foo => %s" % self.app.pargs.foo)

    @expose(help="Install all necessary dependencies on the host system, currently only Ubuntu 14.04 is supported.")
    def install_system(self):


        os.chdir("/usr/src")
        subprocess.call("apt-get update && apt-get upgrade -y", shell=True)
        subprocess.call("apt-get install php5-cli", shell=True)
        subprocess.call("curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar", shell=True)
        subprocess.call("php wp-cli.phar --info --allow-root", shell=True)
        subprocess.call("chmod +x wp-cli.phar", shell=True)
        subprocess.call("mv wp-cli.phar /usr/local/bin/wp", shell=True)

        if os.path.isfile("/etc/init.d/docker"):
            self.app.log.info("Docker is installed.")
        else:
            subprocess.call("wget -qO- https://get.docker.com/ | sh")

        self.call("service docker start")


    @expose(help="Pull all the necessary images to deploy WP on your box.")
    def pull(self):
        self.app.log.info("In order for this to work you need Docker running.")
        subprocess.call("docker pull etopian/nginx-proxy", shell=True)
        subprocess.call("docker pull etopian/alpine-php-nginx-wordpress", shell=True)
        subprocess.call("docker pull mariadb", shell=True)


    @expose(help="Install WP on this box using a certain domain.")
    def install_wp(self):
        self.app.log.info("Installing wp to domain")

    #@expose(aliases=['cmd2'], help="more of nothing")
    #def command2(self):
    #    self.app.log.info("Inside MyBaseController.command2()")


class DockerController(CementBaseController):
    class Meta:
        label = 'docker'
        stacked_on = 'base'

    @expose(help='this is some command', aliases=['some-cmd'])
    def second_cmd1(self):
        self.app.log.info("Inside MySecondController.second_cmd1")

    @expose(help="Create and start a new wordpress process")
    def create(self):
        print("Recieved option: foo => %s" % self.app.pargs.domain)
        domain_name = app.pargs.domain
        domain_name_underscore = domain_name.replace('.', '_')

        subprocess.call("docker run -d --name "+domain_name+" -e VIRTUAL_HOST=www."+domain_name+",etopian.com -v /data/sites/etopian.com:/DATA etopian/alpine-php-wordpress", shell=True)

    def proxy(self):
        domain_name = app.pargs.domain

        #docker run -d --name etopian_com -e VIRTUAL_HOST=www.etopian.com,etopian.com -v /data/sites/etopian.com:/DATA etopian/alpine-php-wordpress



class DockerWp(CementApp):
    class Meta:
        label = 'dockerwp'
        base_controller = 'base'
        handlers = [MyBaseController, DockerController]

with DockerWp() as app:
    app.run()
