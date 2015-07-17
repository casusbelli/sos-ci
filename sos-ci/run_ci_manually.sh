#!/bin/sh
#
# Script for manually creating a CI VM instance with complete DevStack and Settings.
# Edit to set instance name, also edit ./ansible/manual_ci.yml to adopt to your
# installation

ansible-playbook ./ansible/manual_ci.yml -e "patchset_ref=master instance_name=manualCI"
