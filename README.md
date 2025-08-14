# SRM Export

Rename [SRM (Steam ROM Manager)](https://github.com/SteamGridDB/steam-rom-manager) exported image file names like `9942969592307515392.tall.jpg` to normal game title file names like `Yoshi's Cookie (USA, Europe).jpg`.

## Overview

When exporting images using SRM, the file names are like `9942969592307515392.tall.jpg`.

SRM also create a `_selections.json` data file with: `"title": "Yoshi's Cookie (USA, Europe)"`, `"filename": "9942969592307515392.tall.jpg"` to define the image file name and the game title, for example:

```json
[
  {
    "title": "Yoshi's Cookie (USA, Europe)",
    "images": {
      "tall": {
        "pool": "Yoshi's Cookie",
        "filename": "9942969592307515392.tall.jpg"
      },
      "long": {
        "pool": "Yoshi's Cookie",
        "filename": "9942969592307515392.long.png"
      },
      "hero": {
        "pool": "Yoshi's Cookie",
        "filename": "9942969592307515392.hero.png"
      },
      "logo": {
        "pool": "Yoshi's Cookie",
        "filename": "9942969592307515392.logo.png"
      },
      "icon": {
        "pool": "Yoshi's Cookie",
        "filename": "9942969592307515392.icon.png"
      }
    }
  },
  ...
]
```

This program copies `9942969592307515392.tall.jpg` to the directory `Imgs` with the new file name `Yoshi's Cookie (USA, Europe).jpg` according to the json file content.

## Usage

If you are familiar with Python and have Python ( > 3.9) installed, you can run the program directly as: `python srm-export.py <your json file>`.

Or, download the executable file `srm-export.exe` (for Windows) or `srm-export` (for MacOS) and run it:
`./srm-export <your json file>`.

Or just drag `_selections.json` file or its directory onto the program icon (on Windows).

And wait for the command line window to prompt completion.

Or open the program directly in console (on Windows and MacOS) and input the path of the json file or directory.

The program will create a directory `Imgs` under the source `_selections.json` directory and copy the images with the correct file names to this directory.

## Arcade Names

For Arcade platform names, the files' names are: "kof97.zip", not "King of Fighters '97.zip" this full name.

And SRM will use MAME dat to determine the right Arcade game name to fill the title filed:

```json
  {
    "title": "The King of Fighters '97 (NGM-2320)",
    "images": {
      "tall": {
        "pool": "The King of Fighters '97",
        "filename": "10137827267775037440.tall.png"
      },
```

So this export tool will get name like: "The King of Fighters '97 (NGM-2320).png", not "kof97.png", to make it match the right ROM file name, you need to use other tools to match and rename the png files. Suggest to get match from file `gamelist.xml` or `miyoogamelist.xml`, using XML tools like EasyXMLEditor or scripts to match them and rename them.

Besides: some Arcade games's name will written in multi names (for different regions), such as: `Zed Blade / Operation Ragnarok`. To avoid `/` as file name (and it's now allowed), this tool will convert it to: `Zed Blade [Operation Ragnarok].png`. So this: `Street Hoop / Street Slam / Dunk Dream (DEM-004 ~ DEH-004)` will be converted to: `Street Hoop [Street Slam] [Dunk Dream (DEM-004 ~ DEH-004)].png`.

## Tips

- If the `Imgs` directory exists and is not empty, the program will report an error, please clear it and retry.
- If the original image file set in json does not exist, the program will prompt and continue, please check. Normally, SRM will not appear in this situation.
- By default, the program copies the image to the `Imgs` directory under the directory where `_selections.json` is located, which can be modified in `config.json`'s `TARGET_DIR` field. And relative paths such as `../Imgs`, `./Imgs` are supported. And absolute paths are supported too, such as `C:\\Users\\username\\Imgs` (Windows) or `/Users/username/Imgs` (MacOS)
- By default, the program will copy `*.tall.jpg` or `png` image, you can modify `config.json`'s `IMG_TYPE` to set other types, such as `"tall", "hero", "long", "logo", "icon"`, but `"tall"` is recommended.
- And can add suffix to new image file, such as EmuELEC will uses `-image.png`, it will generate file: `Yoshi's Cookie (USA, Europe)-image.jpg`, modify `config.json`'s filed `IMG_SUFFIX` to add suffix. No suffix by default.
- If you have development environment, you can use `pyinstaller --onefile srm-export.py` to build the program.
