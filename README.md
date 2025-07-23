# Ansible Roles for PowerDNS

This project provisions the following PowerDNS services:
- PowerDNS Authoritative Server
- PowerDNS Recursor

By default, the role of PowerDNS Authoritative Server is configured to use PostgreSQL as its backend database.

## Prerequisitites
The `requirements.yml` is defined to install PowerDNS dependencies from the Github repositories, sine the galaxy releases are not the latest version of the master branch.
``` sh
ansible-galaxy install -r requirements.yml
```
