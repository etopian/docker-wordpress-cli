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

###NGinx Proxy
This sits in front of all of your sites at port 80 serving all your sites.
```
docker run -d --name nginx -p 80:80 -p 443:443 -v /etc/nginx/htpasswd:/etc/nginx/htpasswd -v /etc/nginx/vhost.d:/etc/nginx/vhost.d:ro -v /etc/nginx/certs:/etc/nginx/certs -v /var/run/docker.sock:/tmp/docker.sock:ro etopian/nginx-proxy
```

###PHP-FPM + Nginx
Each site runs in its own container with PHP-FPM and Nginx instance.
```
docker run -d --name etopian_com -e VIRTUAL_HOST=etopian.com -v /data/sites/etopian.com:/DATA etopian/alpine-php-wordpress
```

##MySQL Database
```
docker run -d --name mariadb -p 172.17.42.1:3306:3306 -e MYSQL_ROOT_PASSWORD=myROOTPASSOWRD -v /data/mysql:/var/lib/mysql mariadb

CREATE DATABASE etopian_com;
CREATE USER 'etopian_com'@'%' IDENTIFIED BY 'mydbpass';
GRANT ALL PRIVILEGES ON  etopian_com.* TO 'etopian_com'@'%';
 ```

###wp-config.php - SSL


```
define('WP_HOME','https://etopian.com');
define('WP_SITEURL','https://etopian.com');
  define('FORCE_SSL_ADMIN', true);
if ($_SERVER['HTTP_X_FORWARDED_PROTO'] == 'https')
       $_SERVER['HTTPS']='on';
```

###wp-config.php
If you need to change the domain of the site put the follow in wp-config.php of your site.
```
define('WP_HOME','http://etopian.com');
define('WP_SITEURL','http://etopian.com');
```

### File ownership
The site on your host needs proper file permissions. You to your site's folder and type the following:
chown -R 100:101 htdocs/
