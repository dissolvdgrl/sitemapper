#!/bin/sh
# Create folders.
[ -e package ] && rm -r package
mkdir -p package/opt
mkdir -p package/usr/share/applications
mkdir -p package/usr/share/icons/hicolor/scalable/apps

#Copy files (change icon names, add lines for non-scaled icons)
cp -r dist/SiteMapper package/opt/SiteMapper
cp sitemapper-icon.svg package/usr/share/icons/hicolor/scalable/apps/sitemapper-icon.svg
cp SiteMapper.desktop package/usr/share/applications

# Change permissions
find package/opt/SiteMapper -type f -exec chmod 644 -- {} +
find package/opt/SiteMapper -type d -exec chmod 755 -- {} +
find package/usr/share -type f -exec chmod 644 -- {} +
chmod +x package/opt/SiteMapper/SiteMapper