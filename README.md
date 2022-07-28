# Read me
### This is a python tool to generate vhosts config file and append hosts for development
### Developed by python3
#### Config file spec (path.conf.json)

```
{
  "os": "osx",    //operating system e.g. osx windows linux
  "server": "apache",    //http server e.g. apache nginx iis
  "paths":
  {
    "vhosts": "/etc/apache2/other/",    //vhosts file path
    "hosts": "/etc/hosts",    //hosts file path
    "wwwRoot": "/Library/WebServer/Documents/"    //web root path
  },
  "indexPath":    //index file path for select
    [
      "/public",
      "/www/public",
      "/Public"
    ]
  ,
  "domain": ".dev.net"    //development domain
}
```
#### Template file spec (vhosts.conf.temp)

```
<VirtualHost *:80>
    ServerName {serverName}    //{serverName} will be replaced by dev domain name
    DocumentRoot {appPath}/    //{serverName} will be replaced by web app path
    <Directory "{appPath}">
        Options FollowSymLinks
        AllowOverride All
        Order allow,deny
        Allow From All
    </Directory>
</VirtualHost>
```

#### Direct use on mac os

`chmod a+x config.py`

`ln -s path to project/config.py /usr/local/bin/webconfig`

**Contact me:**

https://aloha.one

Mail: admin@theadorelee.com


