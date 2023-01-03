from xml.dom import minidom
from images import *
from utils import askDirectoryGUI, zip_directory, get_datadir
from constructor import Card, Widgets
from shutil import rmtree


def main():
    debug_mode = True
    program_name = "BS_ExtBuilder"

    my_datadir = get_datadir() / program_name
    projects_dir = get_datadir() / program_name / "projects"

    try:
        my_datadir.mkdir(parents=True)
        projects_dir.mkdir(parents=True)
    except FileExistsError:
        pass

    op_select_lst = [str(item) for item in [0, 1]]
    print("====================================================")
    print("BS EXTENSION BUILDER for VASSAL")
    print("(0) Download and compile existing BS set")
    print("(1) Compile custom BS set")
    print("(2) List projects")
    print("====================================================")
    op_select = input("Please enter the ID on the right to select operation: ")

    if op_select not in op_select_lst:
        print("Invalid input, exiting program.")
        exit()

    source_directory = "/"
    images_url = "/"
    set_name = ""
    dir_url = ""

    if op_select == "1":
        ############################
        # Fetch Image Source Directory
        # :Rules: Tensei cards should be in a Folder, with "A@" and "B@" prefixes
        # Normal cards should be placed in the source folder, with naming
        ############################
        source_directory = askDirectoryGUI(debug=debug_mode, message="Please select your image source directory")
        if source_directory is None: raise KeyboardInterrupt()

        set_name = os.path.basename(source_directory)

        dir_url = projects_dir / set_name
        try:
            dir_url.mkdir(parents=True)
        except FileExistsError:
            pass

        images_url = dir_url / "images"
        try:
            images_url.mkdir(parents=True)
        except FileExistsError:
            pass


    ############################
    # Make Processed Image directory
    ############################
    makeImgDir(source_directory, images_url)

    ############################
    # Make Card Object list
    ############################
    cards_objlist = []
    for item in os.listdir(images_url):
        print(os.path.join(images_url, item))
        card = Card(os.path.join(images_url, item), projects_dir)
        cards_objlist.append(card)

    widget = Widgets(set_name=set_name)
    xml_build = widget.build(cards_objlist)

    ############################
    # Build buildFile.xml
    ############################
    buildfile_path = os.path.join(dir_url, "buildFile.xml")
    xmlstr = minidom.parseString(xml_build).toprettyxml(indent="   ")
    xmlstr = xmlstr.replace('<?xml version="1.0" ?>', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
    with open(buildfile_path, "w") as f:
        f.write(xmlstr)

    ############################
    # Build extensiondata
    ############################
    extension_xml = widget.build_extensiondata()
    extensiondata_path = os.path.join(dir_url, "extensiondata")
    xmlstr = minidom.parseString(extension_xml).toprettyxml(indent="   ")
    xmlstr = xmlstr.replace('<?xml version="1.0" ?>', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
    with open(extensiondata_path, "w") as f:
        f.write(xmlstr)

    ############################
    # Build moduledata
    ############################
    module_xml = widget.build_moduledata()
    moduledata_path = os.path.join(dir_url, "moduledata")
    xmlstr = minidom.parseString(module_xml).toprettyxml(indent="   ")
    xmlstr = xmlstr.replace('<?xml version="1.0" ?>', '<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
    with open(moduledata_path, "w") as f:
        f.write(xmlstr)

    save_directory = askDirectoryGUI(debug=debug_mode, message="Please select your Vassal Extension Folder")
    if save_directory is None: raise KeyboardInterrupt()
    zip_directory(name=set_name, path=dir_url, savepath=save_directory)

    exit()
    rmtree(dir_url)


if __name__ == "__main__":
    main()
