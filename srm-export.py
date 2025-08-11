import json
import os
import shutil
import sys
import subprocess

config_file = "./config.json"

default_configs = {
    "TARGET_DIR": "./Imgs/",
    "IMG_TYPE": "tall",
    "IMG_SUFFIX": ""
}


def main():
    """
        Main function:
        1. load configs
        2. create target directory
        3. copy images to target directory, with Title as filename
        4. open target directory
    """
    # 0. init config, if config file not exists, create default config json file
    if not os.path.exists(config_file):
        json.dump(default_configs, open(config_file, "w"))

    # 1. load configs from config file, command argument or user input
    configs = json.load(open(config_file))
    target_dir = configs.get("TARGET_DIR", "./Imgs/")
    img_type = configs.get("IMG_TYPE", "tall")  # support "tall", "hero", "long", "logo", "icon"
    img_suffix = configs.get("IMG_SUFFIX", "")  # or "-image", if you want filename to be: "Super Mario Bros. (USA) (Rev 1)-image.png

    # get json file path from command line argument
    if len(sys.argv) > 1:
        json_file = sys.argv[1].strip()
    else:
        # if no command line argument, prompt user to input path
        # json_file = "./_selections.json"
        json_file = input("Please input json file (or directory) path: ").strip().strip("'").strip("\"")

    # if json file not exists, exit
    if not os.path.exists(json_file):
        print(f"Input file not exists: {json_file}")
        sys.exit(1)

    # if input file is not `_selections.json`, exit
    if os.path.isfile(json_file) and os.path.basename(json_file) != "_selections.json":
        print(f"json file must be `_selections.json`, selected: {json_file}")
        sys.exit(1)

    # if json file is a directory, find "_selections.json" file in it
    if os.path.isdir(json_file):
        json_file = os.path.join(json_file, "_selections.json")
        if not os.path.exists(json_file):
            print(f"json file not exists: {json_file}")
            sys.exit(1)

    source_dir = os.path.dirname(os.path.abspath(json_file))
    # target_dir support relative path and absolute path
    if target_dir.startswith("./") or target_dir.startswith("../"):
        target_dir = os.path.normpath(os.path.join(source_dir, target_dir))
    elif not os.path.isabs(target_dir):
        target_dir = os.path.join(source_dir, target_dir)
    else:
        target_dir = os.path.normpath(target_dir)

    # 2. create target directory
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    elif os.listdir(target_dir):
        print(f"target directory is not empty, please check and clean it: {target_dir}")
        sys.exit(1)

    print(f"source dir: {source_dir}, target dir: {target_dir}")

    count = 0

    # 3. read json file and copy files
    with open(json_file) as f:
        data = json.load(f)

        for index, item in enumerate(data):
            # get title and filename
            game_title = item.get("title")
            node_images = item.get("images", {})
            if not node_images:
                continue
            node_image = node_images.get(img_type, {})
            if not node_image:
                continue
            image_filename = node_image.get("filename", None)
            if not image_filename:
                continue

            # if source image file does not exist, skip
            source_file = os.path.join(source_dir, image_filename)
            if not os.path.exists(source_file):
                print(f"Warning! Source file not exists: {source_file}")
                continue
            image_file_ext = os.path.splitext(image_filename)[1]

            # replace ": " to " - ", eg: "Cyberbots: Fullmetal Madness"
            game_title = game_title.replace(" : ", " - ").replace(": ", " - ").replace(":", " - ")

            # set target file path and file name
            # test if target filename is Arcade name and has multi names with " / "
            if " / " in game_title:
                # But sometime you will get name like: Contra (US / Asia, set 1), or: Aero Fighters (World / USA + Canada / Korea / Hong Kong / Taiwan) (newer hardware), it has to be ignored, and replace " / " with ", "

                # and will support multi " / " to convert "A / B / C" to "A [B] [C].png"
                ts = game_title.split(" / ")
                # to determine if it's multi " / " for regions. Test if the count of "(" and ")" is equal
                if ts[0].count("(") == ts[0].count(")"):
                    game_title = ts[0]
                    for t in ts[1:]:
                        game_title += f" [{t}]"
                else:
                    # print(f"Warning! Multi \" / \" region detected: {game_title}, ignored.")
                    game_title = game_title.replace(" / ", ", ")

            #     print(f"get: {game_title}")
            # continue

            target_filename = game_title + img_suffix + image_file_ext
            target_filepath = os.path.join(target_dir, target_filename)

            # if target file already exists, skip
            if os.path.exists(target_filepath):
                print(f"Warning! Target file already exists: {target_filepath}")
                continue

            # copy file
            try:
                shutil.copy2(source_file, target_filepath)
                print(f"File {index + 1}: copied \"{image_filename}\" to \"{target_filename}\"")
                count += 1
            except Exception as e:
                print(f"Error!!! when copying file: \"{image_filename}\" to \"{target_filename}\": {e}")
                continue

    print(f"Done! Total copied files: {count}")

    # 4. All Done! try to open File Explorer (on Windows) or Finder (on MacOS) of the target directory
    try:
        if os.name == 'nt':
            # Windows
            os.startfile(target_dir)
        elif os.name == 'posix':
            # MacOS, Linux
            subprocess.call(['open' if os.uname().sysname == 'Darwin' else 'xdg-open', target_dir])
        else:
            print(f"Unsupported OS: {os.name}")
            return
    except Exception as e:
        print(f"Error when opening directory: {e}")
        return


# test
if __name__ == "__main__":
    test_file = r'/Users/yinguowei/Roms (tiny-best-set-go)/_TODO/NEOGEO/srm-image-choices1/_selections.json'
    # test_file = r'/Users/yinguowei/Roms (tiny-best-set-go)/_TODO/ARCADE/srm-image-choices/_selections.json'
    sys.argv.append(test_file)
    main()
