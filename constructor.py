import os
from xml.etree.ElementTree import Element, SubElement, tostring
from images import isImage, countImagesIn
from datetime import datetime, timezone
from shutil import move


class Card:
    # Tasks: Create contained methods without accessing datatypes outside the function
    # Create methods to access values
    def __init__(self, image_path, project_path):
        self.image_path = image_path
        self.tensei = False
        basename = os.path.basename(image_path)

        if isImage(image_path):
            self.filename = [basename]

        elif os.path.isdir(image_path):
            if countImagesIn(image_path) == 2:
                images_directory = project_path / "images"

                tensei_faces = os.listdir(image_path)
                tensei_faces_filtered = []

                for item in tensei_faces:
                    if "@" in item and isImage(item):
                        tensei_faces_filtered.append(item)
                        path = os.path.join(image_path, item)
                        print(path, images_directory)
                        move(path, images_directory)

                os.rmdir(image_path)
                tensei_faces_filtered.sort()
                self.filename = tensei_faces_filtered
                self.tensei = True
        else:
            self.filename = None
            self.cardname = None
            return

        if self.tensei:
            removed_prefix = [item.split('@', 1)[1] for item in self.filename]
            self.cardname = [item.replace('.png', '').replace('.jpeg', '').replace('.jpg', '') for item in
                             removed_prefix]
        else:
            self.cardname = [item.replace('.png', '').replace('.jpeg', '').replace('.jpg', '') for item in
                             self.filename]


class Widgets:
    def __init__(self,
                 set_name=None,
                 description=None,
                 extensionId=None,
                 module=None,
                 moduleVersion=None,
                 vassalVersion=None,
                 version=None):
        utc_dt = datetime.now(timezone.utc)

        ####################################
        # Initialise parameter values      #
        ####################################
        self.set_name = set_name
        if set_name is None:
            self.set_name = "Custom"

        self.description = description
        if description is None:
            time = utc_dt.astimezone().isoformat()
            self.description = f"Update: {time}"

        self.extensionId = extensionId
        if extensionId is None:
            self.extensionId = "fff"

        self.module = module
        if module is None:
            self.module = "Battle Spirits [Online Battlers]"

        self.moduleVersion = moduleVersion
        if moduleVersion is None:
            self.moduleVersion = "1.0"

        self.vassalVersion = vassalVersion
        if vassalVersion is None:
            self.vassalVersion = "3.6.7"

        self.version = version
        if version is None:
            self.version = "1.0"

    def build(self, cards=None):
        ####################################
        # Initialise XML file              #
        ####################################
        root = Element('VASSAL.build.module.ModuleExtension')
        root.attrib = {"anyModule": "false",
                       "description": str(self.description),
                       "extensionId": str(self.extensionId),
                       "module": str(self.module),
                       "moduleVersion": str(self.moduleVersion),
                       "nextPieceSlotId": "515",
                       "vassalVersion": str(self.vassalVersion),
                       "version": str(self.version)}

        declare_tab = SubElement(root, "VASSAL.build.module.ExtensionElement")
        declare_tab.attrib = {"target": "VASSAL.build.module.PieceWindow:Library/VASSAL.build.widget.TabWidget"}

        saga_tab = SubElement(declare_tab, "VASSAL.build.widget.TabWidget")
        saga_tab.attrib = {"entryName": str(self.set_name)}

        set_tab = SubElement(saga_tab, "VASSAL.build.widget.ListWidget")
        set_tab.attrib = {"divider": "566",
                          "entryName": self.set_name,
                          "height": "-56",
                          "scale": "1.0",
                          "width": "-10"}

        for card in cards:
            # Card Object attrib initialise
            attrib = {
                "entryName": card.cardname[0],
                "gpid": "25e:151",
                "height": "490",
                "width": "350"
            }

            if card.tensei:
                xml_text = f"+/null/prototype;Card	" \
                           f"emb2;Flip;128;A;;128;;;128;;;;1;false;0;0;" \
                           f"{card.filename[1]};" \
                           f"{card.cardname[1]};true;;;;false;;1;1;false;65,130;;;;1.0\	piece;;;" \
                           f"{card.filename[0]};" \
                           f"{card.cardname[0]}/	-1\	null;0;0;;0"

                SubElement(set_tab, "VASSAL.build.widget.PieceSlot", attrib=attrib).text = xml_text
            else:
                xml_text = f"+/null/prototype;Card	piece;;;{card.filename[0]};{card.cardname[0]}/	null;0;0;;0"
                SubElement(set_tab, "VASSAL.build.widget.PieceSlot", attrib=attrib).text = xml_text

        return tostring(root)

    def build_extensiondata(self):
        root = Element('data', version="1")
        version = SubElement(root, "version")
        version.text = self.version

        vassal_version = SubElement(root, "VassalVersion")
        vassal_version.text = self.vassalVersion

        date_saved = SubElement(root, "dateSaved")
        date_saved.text = "1662110307672"

        description = SubElement(root, "description")
        description.text = self.description

        universal = SubElement(root, "universal")
        universal.text = "false"
        return tostring(root)

    def build_moduledata(self):
        root = Element('data', version="1")
        version = SubElement(root, "version")
        version.text = "1.0"

        vassal_version = SubElement(root, "VassalVersion")
        vassal_version.text = self.vassalVersion

        date_saved = SubElement(root, "dateSaved")
        date_saved.text = "1662110307672"

        description = SubElement(root, "description")
        description.text = self.description

        name = SubElement(root, "name")
        name.text = self.module
        return tostring(root)
