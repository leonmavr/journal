# Arch Linux tips

## 1. Restore previous version of an installed package

Sometimes when a package is upgraded the current configs are not supported anymore and the program doesn't work as expected. This was the case when I upgrade rofi to higher than 1.6.0. Arch package manager (pacman) keeps diffs of the current package compared to its previously installed versions in:
```
/var/cache/pacman/pkg
```
To restore, let's say rofi, to the previously installed version do:
```
yay -U /var/cache/pacman/pkg/rofi-1.6.0-1-x86_64.pkg.tar.zst
```
To go one step further, let's say that we don't want rofi to be further updated. Then edit pacman's config:
```
sudo edit /etc/pacman.conf
```
Find the `IgnorePkg` line and uncomment it, then add your package on the RHS.
```
#IgnorePkg = 
```
This becomes:
```
IgnorePkg = rofi 
```

## 2. File xxx is corrupted invalid signature

If you get this message while installing a package, the cage is often an outdate keyring file.  
To update it, do:
```
sudo pacman -Sy archlinux-keyring
```
