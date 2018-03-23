Base station
=====

The base sataion configuration can be broken down into multiple tasks:

- [Raspberry Pi Configuration](#raspberry-pi-configuration)
	- [General Configuration](#general-configuration)
	- [Security Setup](#security-setup)
	- [Backports Configuration](#backports-configuration)
- [Router Configuration](#router-configuration)
- [Connecting the Two](#connecting-the-two)


# Raspberrry Pi Configuration

The bulk of the setup process on the Raspberry Pi can be done using the pre-made configuration files found here. All of these tasks are based on running from a blank image of [raspbian strech lite](https://www.raspberrypi.org/downloads/raspbian/).

**STOP** before proceeding be sure to change the default password. In its default configuration the password is `raspberry` it is critical that this is changed using the `passwd` command.

## General Configuration

Before jumping into configuring the individual applications there are some general security configurations and applications which must be installed.

First off we will configure the Pi to use the entire SD card. To do so run `sudo raspi-config` and choose the `expand filesystem` option. This will expand the FS to use the entirty of the SD card.

While you're in the configuration menu you can also enable the SSH service. This can be found under the `interfacing options` menu. SSH will allow administrators such as yourself to more easily modify settings and configurations on the raspberry pi in the future.

## Backports Setup

Before adding the backports repository you will need to trust the signing keys. To do so use the following commands:

```bash
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 7638D0442B90D010
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 8B48AD6246925553
```

Next you're going to need to update the sources using the following command:

`echo 'deb http://ftp.debian.org/debian stretch-backports main' | sudo tee -a /etc/apt/sources.list.d/strech-backports.list`

Lastly you will need to update your package lists using:

`sudo apt-get update`

Now you will be able to install packages from the backports repository, which is reuqired for some of Freeradius' dependencies.


## Required Applications

The base station relies on plenty of applications which can be installed using the following command:


```bash
sudo apt-get install dnsmasq freeradius ufw nginx mariadb-server freeradius-mysql
```

After installation many of these applications will require configuration which will take place later.

## Security Setup

Since we're runing in a hospital environment it is critical to ensure proper security measures are in place. This involves blocking access to ports, generating SSL certificates, (optionally) configurating SSH to only allow access via keys.

```bash
sudo ufw allow 22 53 80 443 1812 && sudo ufw enable
```

Uncomplicated firewall (ufw) will allow access to the required ports while blocking access to all other ports. These ports are reuired for normal operation and will be properly configured to serve content securly.

Below is a table explaining why said ports are open.

| Port | Reason |
|------|--------|
| 22   | SSH    |
| 53   | DNS    |
| 80   | HTTP   |
| 443  | HTTPS  |
| 1812 | Radius |


Configuring the SSL certificate can be found in the [Nginx setup](#nginx-setup) step.

## Nginx Setup

Nginx is our webserver of choice. It is responsible for serving up the REST API as well as the Nurse and Administraive interfaces

### Directory Setup

In our configuration everything is based off of "virtual" hosts. Each of the various apps (API, nurse device, Admin panel) all run from an individual

## FreeRadius Setup

To authenticate users to the WPA-2 Enterprise Freeradius must be configured to accept connection requests from the router at `192.168.1.1`. It should also be noted that the radius server is listening on `192.168.1.10`.

### Setup MySQL DB

The MySQL freeradius database must be configured manually. In our case we're using Freeradius 3.x so this [tutorial](https://wiki.freeradius.org/guide/SQL-HOWTO-for-freeradius-3.x-on-Debian-Ubuntu) can be used to setup the database. It must be noted that in the tutorial they constantly reference `/etc/raddb`

### Testing Freeradius

As seen in MySQL setup tutorial, once the database has been setup a user can be added using the following commands:

```
mysql -u radius -p
use radius;
insert into radcheck (username,attribute,op,value) values("test", "Cleartext-Password", ":=", "test");
```

This will create a user with the credentials `test/test`. To test the connection a freeradius debug instance can be started using `freeradius -X`. *NOTE* the freeradius dameon must be stopped first, this can be done using `sudo service freeradius stop`.

Next the `radcheck` command can be used to test if the server is listening properly.

### Sample Freeradius Code

A few code snippets have been created which demonstrate how to perform actions against the Freeradius MySQL database. These pieces of sample code can be found within the [freeradius_api](freeradius_api) directory.

## Setup Python Environment

```
virtualenv -p /usr/bin/python3 yourenv
source yourenv/bin/activate
pip3 install mysql-connector
```

# Router Configuration

The router serves as the main wireless access point. We must configure it to serve wireless over WPA-2 Enterprise with the Raspberry Pi acting as the Radius server.

## DHCP Server configuration

# Connecting the Two
