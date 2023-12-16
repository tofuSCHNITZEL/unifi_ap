# unifi_ap

Python API for UniFi accesspoints

## Installation

* pip install unifi_ap

## Usage

currently this package can only be used by importing it into own python files

```
import unifi_ap
ap = unifi_ap.UniFiAP("10.0.0.253", "admin")
clients = ap.get_clients()
ssids = ap.get_ssids()
clients_for_ssid = ap.get_clients(for_ssids=["guest"])
```

* Address/hostname and username are mandatory  
* if you don't define a password, ssh keys from the local ssh authentication agent are used  
* in addition/alternative to a password you can also define a private key file to be used for the authentication

`UniFiAP("10.0.0.253", "admin", keyfile="my-rsa.key")`

## Features

* get a list of SSIDs that the accesspoint is serving
* get currently connected clients (you can specify the SSIDs for which you want to get the clients - default: all)

## Credits

* inspired by https://pypi.org/project/unifi-tracker/

## License

[MIT](https://choosealicense.com/licenses/mit/)
