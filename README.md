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

## Tips

- If the `Imgs` directory exists and is not empty, the program will report an error, please clear it and retry.
- If the original image file set in json does not exist, the program will prompt and continue, please check. Normally, SRM will not appear in this situation.
- By default, the program copies the image to the `Imgs` directory under the directory where `_selections.json` is located, which can be modified in `config.json`'s `TARGET_DIR` field. And relative paths such as `../Imgs`, `./Imgs` are supported. And absolute paths are supported too, such as `C:\\Users\\username\\Imgs` (Windows) or `/Users/username/Imgs` (MacOS)
- By default, the program will copy `*.tall.jpg` or `png` image, you can modify `config.json`'s `IMG_TYPE` to set other types, such as `"tall", "hero", "long", "logo", "icon"`, but `"tall"` is recommended.
- And can add suffix to new image file, such as EmuELEC will uses `-image.png`, it will generate file: `Yoshi's Cookie (USA, Europe)-image.jpg`, modify `config.json`'s filed `IMG_SUFFIX` to add suffix. No suffix by default.
