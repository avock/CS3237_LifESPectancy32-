- a systemd of `mqtt_server.service` is being run, view it under `/etc/systemd/system/mqtt_server.service`
- couple of useful commands when debugging the systemd:
    - `sudo systemctl start mqtt_server.service` to start the systemd
    - `sudo systemctl status mqtt_server.service` to check the systemd status
    - `sudo systemctl stop mqtt_server.service` to stop the systemd 
    - `sudo systemctl enable mqtt_server.service` to enable/disable the systemd (would likely not be using this)
    UPDATE: all these commands are simplified to `mqtt-XXX`, config can be found in `~/.bashrc`
- use `sudo journalctl -u mqtt_server.service` to read logs (add -fu tag to read in real-time)