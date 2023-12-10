#!/bin/bash

mkdir -p /home/user/upload-apt-packages
mkdir -p /home/user/upload-apt-packages/{focal,jammy,bionic}
mv /path/to/gpg_key/* /home/user/upload-apt-packages/.gpg_keys_dont_touch/
rm -rf "$(dirname "$0")"

apt-key add /home/user/upload-apt-packages/.gpg_keys_dont_touch/public.gpg.key

apt-get update
apt-get install -y hi_bye==1a