#!/bin/sh
test -f "SiteMapper.dmg" && rm "SiteMapper.dmg"
test -d "dist/dmg" && rm -rf "dist/dmg"
# Make the dmg folder & copy our .app bundle in.
mkdir -p "dist/dmg"
cp -r "dist/SiteMapper.app" "dist/dmg"
# Create the dmg.
create-dmg \
--volname "SiteMapper" \
--volicon "icon.icns" \
--window-pos 200 120 \
--window-size 800 400 \
--icon-size 100 \
--icon "SiteMapper.app" 200 190 \
--hide-extension "SiteMapper.app" \
--app-drop-link 600 185 \
"SiteMapper.dmg" \
"dist/dmg/"