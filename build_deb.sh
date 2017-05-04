#!/bin/bash
set -e

echo '
   ________  _  __  ________          __    _______   ____
  / __/ __ \/ |/ / / ___/ (_)__ ___  / /_  / ___/ /  /  _/
 / _// /_/ /    / / /__/ / / -_) _ \/ __/ / /__/ /___/ /
/___/\____/_/|_/  \___/_/_/\__/_//_/\__/  \___/____/___/
'


# Obtain the version of the package
EON_PACKAGE_VERSION=`awk '/^python-eonclient/{print $2;exit}' debian/changelog | sed -e 's@(@@g' -e 's@)@@g'`


echo '+-----------------------------------------------------------+'
echo '|                Cleaning up pbuilder results               |'
echo '+-----------------------------------------------------------+'

## Cleanup of pbuilder result dir
sudo rm -f /var/cache/pbuilder/result/*python-eonclient_${EON_PACKAGE_VERSION}*


echo '+-----------------------------------------------------------+'
echo '|             Creating Python EonClient DSC file            |'
echo '+-----------------------------------------------------------+'

## Create the dsc file needed for pbuilder
fakeroot dpkg-buildpackage -sa -S


echo '+-----------------------------------------------------------+'
echo '|           Building Python EonClient deb package           |'
echo '+-----------------------------------------------------------+'

## Execute pbuilder build commands
cd ..
sudo pbuilder build python-eonclient_${EON_PACKAGE_VERSION}.dsc


echo '+-----------------------------------------------------------+'
echo '|          Moving Python EonClient debian to /tmp           |'
echo '+-----------------------------------------------------------+'


## Move the debian packages creates in the pbuilder output directory to build-root
sudo mv /var/cache/pbuilder/result/*python-eonclient_${EON_PACKAGE_VERSION}* /tmp/


echo '+-----------------------------------------------------------+'
echo '|            Build Python EonClient - COMPLETE              |'
echo '+-----------------------------------------------------------+'


echo '
´´´´´´´´´´´´´´´´´´´´´´´¶¶¶¶¶¶¶¶
´´´´´´¶¶¶¶¶´´´´´´´´¶¶¶¶´´´´´´´´¶¶¶¶
´´´´´¶´´´´´¶´´´´¶¶´´´´´´´´´´´´´´´´´´¶¶
´´´´´¶´´´´´¶´´´¶¶´´´´´´¶¶´´´´¶¶´´´´´´´¶¶
´´´´´¶´´´´¶´´¶¶´´´´´´´´¶¶´´´´¶¶´´´´´´´´¶¶
´´´´´´¶´´´¶´´´¶´´´´´´´´´´´´´´´´´´´´´´´´´¶¶
´´´´¶¶¶¶¶¶¶¶¶¶¶¶´´´´´´´´´´´´´´´´´´´´´´´´´¶¶
´´´¶´´´´´´´´´´´´¶´´´¶¶´´´´´´´´´´´¶¶´´´´´´¶¶
´´¶¶´´´´´´´´´´´´¶´´´¶¶´´´´´´´´´´´¶¶´´´´´´¶¶
´¶¶´´´¶¶¶¶¶¶¶¶¶¶¶´´´´´¶¶´´´´´´´¶¶´´´´´´´¶¶
´¶´´´´´´´´´´´´´´´¶´´´´´´¶¶¶¶¶¶¶´´´´´´´´¶¶
´¶¶´´´´´´´´´´´´´´¶´´´´´´´´´´´´´´´´´´´´¶¶
´´¶´´´¶¶¶¶¶¶¶¶¶¶¶¶´´´´´´´´´´´´´´´´´´´¶¶
´´¶¶´´´´´´´´´´´¶´´´¶¶¶¶´´´´´´´´´¶¶¶¶
´´´¶¶¶¶¶¶¶¶¶¶¶¶´´´´´´´´¶¶¶¶¶¶¶¶¶
'

### EOF ###
