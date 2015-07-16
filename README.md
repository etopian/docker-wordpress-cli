# docker-wordpress-cli
A Python based CLI to help you deploy WordPress on Docker using nginx-proxy and Alpine Linux.

This is a work in progress. Current aim is to only support Ubuntu 14.04 LTS.

This deploys the site on the host system under /data/sites/domain.tld, this is then published to the container using the -v switch. This makes sure your data for your site is available in one place outside of your container in case you decide to delete the container when upgrading, etc. A Docker volume seems like a big black box to stuff your data inside which can easily be deleted.

Similarly MySQL/MariaDB data is stored under /data/mysql on the host and mounted using -v again so if you decide to upgrade your MySQL the data is not destroyed.

It will then install the site for you as well.

We use the following images:

* https://github.com/etopian/php-wordpress
* https://github.com/etopian/nginx-proxy
* 
Mail is not routed by the container, you must use an SMTP plugin or Mailgun or AWS SES to route your site's email.
