# GLAuth Snap
This repository contains the packaging metadata for creating a snap of GLAuth.  For more information on snaps, visit [snapcraft.io](https://snapcraft.io/). 

## Installing the Snap
The snap can be installed directly from the Snap Store.  Follow the link in the badge below for more information.
<br>

[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/glauth)


## Building the Snap
The steps outlined below are based on the assumption that you are building the snap with the latest LTS of Ubuntu.  If you are using another version of Ubuntu or another operating system, the process may be different.

### Clone Repository
```bash
git clone git@github.com:dvdgomez/glauth-snap.git
cd glauth-snap
```
### Installing and Configuring Prerequisites
```bash
sudo snap install snapcraft
sudo snap install lxd
sudo lxd init --auto
```
### Packing and Installing the Snap
```bash
snapcraft pack
sudo snap install ./glauth*.charm --devmode
```
## How to Use the Snap
By default, when the snap is installed the daemon will be disabled. This is done to allow the user to first provide the glauth configuration files, server key and certificate. Can read more about glauth configuration here: https://glauth.github.io/docs/backends.html 
```bash
# $SNAP_COMMON = /var/snap/glauth

# GLAuth expects a glauth.key key
$SNAP_COMMON/etc/glauth/keys.d/glauth.key
# GLAuth expects a glauth.crt certificate
$SNAP_COMMON/etc/glauth/certs.d/glauth.crt
# GLAuth configs go here
$SNAP_COMMON/etc/glauth/glauth.d/

# To create the key and certificate
openssl req -x509 -newkey rsa:4096 -keyout $SNAP_COMMON/etc/glauth/keys.d/glauth.key -out $SNAP_COMMON/etc/glauth/certs.d/glauth.crt -days 365 -nodes -subj "/CN=`hostname`"
```

Once everything is in place, the daemon can be started and enabled:
```bash
snap start glauth --enable
```

To restart with a new configuration:
```bash
snap stop glauth

# Replace configuration as needed

snapctl restart glauth --enable
```

## License
The GLAuth Snap is free software, distributed under the Apache Software License, version 2.0. See [LICENSE](https://github.com/dvdgomez/glauth-snap/blob/main/LICENSE) for more information.
