"""Communicate with an UniFi accesspoint"""

import json
import paramiko
from typing import Any


class UniFiAPConnectionException(Exception):
    """Exception indicating problems with the connection to the accespoint"""

    def __init__(self, message):
        super().__init__(message)


class UniFiAPDataException(Exception):
    """Exception indicating problems with the data returned from the accespoint"""

    def __init__(self, message):
        super().__init__(message)


class UniFiAP:
    """Communicate with an UniFi accesspoint"""

    def __init__(
        self,
        target: str,
        username: str,
        password: str | None = None,
        key_file: str | None = None,
        port: int = 22,
        timeout: int = 30,
    ) -> None:
        self.unifi_data_cmd = "mca-dump"
        self.unifi_ssid_array = "vap_table"
        self.unifi_client_array = "sta_table"
        self.target = target
        self.username = username
        self.password = password
        self.key_file = key_file
        self.port = port
        self.timeout = timeout

    def _fetch_ap_data(self) -> dict:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

        try:
            client.connect(
                hostname=self.target,
                port=self.port,
                username=self.username,
                password=self.password,
                key_filename=self.key_file,
                timeout=self.timeout,
            )
            _, stdout, _ = client.exec_command(self.unifi_data_cmd)
            out = stdout.read()
            jresult = json.loads(out.decode("utf-8"))
        except (paramiko.SSHException, TimeoutError, FileNotFoundError) as e:
            raise UniFiAPConnectionException(str(e)) from None
        except ValueError as e:
            raise UniFiAPDataException(str(e)) from None
        finally:
            client.close()

        return jresult

    def get_ssids(self) -> set | None:
        """Returns all SSIDs from the accesspoint"""
        ap_data = self._fetch_ap_data()
        ssids: set[str] = set()

        if self.unifi_ssid_array not in ap_data:
            raise UniFiAPDataException(
                "device did not return any vap_table data - is it an accesspoint?"
            )

        for vap in ap_data[self.unifi_ssid_array]:
            ssids.add(vap.get("essid"))

        return ssids

    def get_clients(self, for_ssids: list | None = None) -> dict | None:
        """Returns all clients from the accesspoint connected to any or certain SSIDs"""
        ap_data = self._fetch_ap_data()
        clients: dict[str, dict[str, Any]] = {}

        if self.unifi_ssid_array not in ap_data:
            raise UniFiAPDataException(
                "device did not return any vap_table - is it an accesspoint?"
            )

        for vap in ap_data[self.unifi_ssid_array]:
            if not for_ssids or vap.get("essid") in for_ssids:
                client_data = vap.get(self.unifi_client_array)
                if client_data:
                    for client in client_data:
                        clients.update({client.get("mac"): client})

        return clients
