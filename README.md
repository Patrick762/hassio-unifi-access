# hassio-unifi-access
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![Validate with hassfest](https://github.com/Patrick762/hassio-unifi-access/actions/workflows/hassfest_validation.yml/badge.svg)](https://github.com/Patrick762/hassio-solvis-modbus/actions/workflows/hassfest_validation.yml)
[![HACS Action](https://github.com/Patrick762/hassio-unifi-access/actions/workflows/HACS.yml/badge.svg)](https://github.com/Patrick762/hassio-solvis-modbus/actions/workflows/HACS.yml)

Unifi Access Integration for Home Assistant

## Disclaimer
This integration is provided without any warranty or support by Ubiquiti. I do not take responsibility for any problems it may cause in all cases. Use it at your own risk.

## Installation
To install this integration, you first need [HACS](https://hacs.xyz/) installed.
After the installation, you need to add the repository URL in HACS as custom repository: https://github.com/Patrick762/hassio-unifi-access
You can then search for "Unifi Access" in the HACS integrations.

## Adding devices
You can add devices via the home assistant integrations page by using the console ip address and token (Unifi Access Settings -> General -> Advanced -> API Token).

### Available sensors

- Door open / closed
- Door locked / unlocked
