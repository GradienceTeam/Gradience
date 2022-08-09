<img align="left" alt="Project logo" src="data/icons/hicolor/scalable/apps/com.github.AdwCustomizerTeam.AdwCustomizer.svg" />

# Adwaita Manager
Change the look of Adwaita, with ease

![Screenshot of interface with Adwaita light theme](pictures/main_screenshot.png)

Adwaita Manager (AdwCustomizer) is a tool for customizing Libadwaita applications and the adw-gtk3 theme.

<details>
  <summary>More screenshots</summary>
  
  ![Screenshot of interface with a customized theme](pictures/customized_screenshot.png)
  
  ![Screenshot of proof that this actually works](pictures/proof_of_work_screenshot.png)
</details>

## Building and Installing
1. Open Terminal
2. Run `git clone https://github.com/AdwCustomizerTeam/AdwCustomizer.git && cd AdwCustomizer`
3. Add the `gnome-nightly` Flatpak repository `flatpak remote-add --if-not-exists gnome-nightly https://nightly.gnome.org/gnome-nightly.flatpakrepo`
4. Install the `master` version of GNOME SDK: `flatpak install org.gnome.Sdk/x86_64/master org.gnome.Platform/x86_64/master`
5. Run `flatpak-builder --install --user --force-clean repo/ com.github.AdwCustomizerTeam.AdwCustomizer.json`

Alternatively, open the project with GNOME Builder, then build and run it.

## Setup Tutorial

### Libadwaita applications
No additional setup is required for native Libadwaita applications.

For Flatpak Libadwaita applications, you need to override their permissions:
- Run `sudo flatpak override --filesystem=xdg-config/gtk-4.0` or
- Use [Flatseal](https://github.com/tchx84/Flatseal) and adding `xdg-config/gtk-4.0` to **Other files** in the **Filesystem** section of **All Applications**

### Vanilla GTK 4 applications
Use [this guide](https://github.com/lassekongo83/adw-gtk3/blob/main/gtk4.md) to theme vanilla GTK 4 applications.

### GTK 3 applications
- Install and apply the [adw-gtk3](https://github.com/lassekongo83/adw-gtk3#readme) theme (don't forget to install the Flatpak package!)
- For Flatpak applications, you need to override their permissions:
  - Run `sudo flatpak override --filesystem=xdg-config/gtk-3.0` or
  - Use [Flatseal](https://github.com/tchx84/Flatseal) and adding `xdg-config/gtk-3.0` to **Other files** in the **Filesystem** section of **All Applications**

## Roadmap
This tool is currently WIP, but it already has a plenty of features and is very usable. Below is the roadmap, where all the checked features are already implemented:

- [x] Customize named colors, either with a color picker or with text
- [x] Explanations for some named colors
- [x] Partial theme preview
- [x] Built-in presets for Adwaita and Adwaita Dark (based on default libadwaita colors)
- [x] Apply changes to libadwaita, GTK4 (with extracted libadwaita theme) and GTK3 (with the adw-gtk3 theme) applications
- [x] Load and create custom presets
- [x] View adw-gtk3's support of variables
- [x] View parsing errors
- [x] Customize palette colors
- [x] Add custom CSS code
- [x] Localization support
- [x] Normalize color variables
- [ ] Make the code more secure
- [ ] Release on Flathub
- [ ] Full theme preview
- [ ] Customize GNOME Shell
- [ ] Customize GDM
- [ ] Customize KvLibadwaita
- [ ] Customize Firefox GNOME theme

## Contribute
### Code
Fork this repository, then create a push request when you're done adding features or fixing bugs.

### Localize
The localization project is available on [Transifex](https://www.transifex.com/adwcustomizerteam/adwcustomizer/). 

