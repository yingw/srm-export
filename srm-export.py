import json
import os
import shutil
# import regex as re
import sys

config_file = "./config.json"

# if config file not exists, create default config json file
if not os.path.exists(config_file):
    configs = {
        "TARGET_DIR": "./Imgs/",
        "IMG_TYPE": "tall",
        "IMG_SUFFIX": ""
    }
    json.dump(configs, open(config_file, "w"))

# load configs
configs = json.load(open(config_file))
target_dir = configs.get("TARGET_DIR", "./Imgs/")
# if re.search(r'[^/\0:]', target_dir):
#     print("Error!!! cannot contain special characters '\\0' or ':', {target_dir}")
# sys.exit(1)
img_type = configs.get("IMG_TYPE", "tall")  # support "tall", "hero", "long", "icon"
img_suffix = configs.get("IMG_SUFFIX", "")  # or "-image", if you want file like: "Super Mario Bros. (USA) (Rev 1)-image.png

# get json file path from command line argument
if len(sys.argv) > 1:
    json_file = sys.argv[1].strip()
else:
    # if no command line argument, prompt user to input path
    # json_file = "./_selections.json"
    json_file = input("Please input json file (or directory) path: ").strip()

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
    # if "_selections.json" not exists, exit
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

if not os.path.exists(target_dir):
    os.makedirs(target_dir)
elif os.listdir(target_dir):
    print(f"target dir is not empty, please check and clean it: {target_dir}")
    sys.exit(1)

print(f"source dir: {source_dir}, target dir: {target_dir}")

count = 0

with open(json_file) as f:
    data = json.load(f)

    for index, item in enumerate(data):
        # get title and filename
        title = item.get("title")
        filename = item.get("images", {}).get(img_type, {}).get("filename", None)
        if not filename:
            continue

        # if source file not exists, skip
        source_file = os.path.join(source_dir, filename)
        if not os.path.exists(source_file):
            print(f"Warning! Source file not exists: {source_file}")
            continue
        ext = os.path.splitext(filename)[1]

        # set target file path and file name
        target_filename = title + img_suffix + ext
        target_file = os.path.join(target_dir, target_filename)

        # if target file already exists, skip
        if os.path.exists(target_file):
            print(f"Warning! Target file already exists: {target_file}")
            continue

        # copy file
        try:
            shutil.copy2(source_file, target_file)
            print(f"File {index + 1}: copied \"{filename}\" to \"{target_filename}\"")
            count += 1
        except Exception as e:
            print(f"Error!!! when copying file: \"{filename}\" to \"{target_filename}\": {e}")
            continue

    print(f"Done! Total copied files: {count}")
