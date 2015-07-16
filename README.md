# Docker Wordpress CLI
A Python based CLI to help you deploy WordPress on Docker using nginx-proxy and Alpine Linux.

**This is a work in progress, not for use. Current aim is to only support Ubuntu 14.04 LTS.**

This deploys the site on the host system under /data/sites/domain.tld, this is then published to the container using the -v switch. This makes sure your data for your site is available in one place outside of your container in case you decide to delete the container when upgrading, etc. A Docker volume seems like a big black box to stuff your data inside which can easily be deleted.

Similarly MySQL/MariaDB data is stored under /data/mysql on the host and mounted using -v again so if you decide to upgrade your MySQL the data is not destroyed.

It will then install the site for you as well.

We use the following images:

* https://github.com/etopian/alpine-php-wordpress
* https://github.com/etopian/nginx-proxy


##Mail
Mail is not routed by the container, you must use an SMTP plugin or Mailgun or AWS SES to route your site's email.
* https://wordpress.org/plugins/wp-ses/
* https://wordpress.org/plugins/mailgun/
* https://wordpress.org/plugins/wp-smtp/
* https://wordpress.org/plugins/easy-wp-smtp/
* https://wordpress.org/plugins/wp-mail-bank/


##Docker WP CLI Commands
* install-system - Install all necessary dependencies on the host system, currently only Ubuntu 14.04 is supported.
* install-wp - Install WP on this box using a certain domain.
* pull - Pull all the necessary images to deploy WP on your box.
* run - Run all images.

##WP-CLI and the Host System

This project install WP-Cli on the host system to perform certain tasks. HOwever, you must not use WP-CLI to interact with the files on the host system. Doing so is very dangerous as if your site becomes compromised and you run WP-Cli on it on the host system you can compromise the host system, or other sites that have the same user. So don't do it! If you need to work on the site, you must run a separate container that uses volumes to mount the site root inside of it. This way running WP-CLI is safe.

In the meantime check out http://www.dockerwordpress.com for instructions on how you can do all the stuff that this is suppose to do manually.
