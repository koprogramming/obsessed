import glob
import os
import shutil
import sys

import markdown
from markdown.extensions.wikilinks import WikiLinkExtension

from CoolWikilinksExtension import CoolWikilinkExtension
from utils import modify_name

OUTPUT_FOLDER = "build"

HEADER = ""
FOOTER = ""


with open("fragments/_foot.html") as f, open("fragments/_head.html") as h:
    HEADER = h.read()
    FOOTER = f.read()


def add_header_and_footer(html_text):
    """
    Adds a header and a footer
    """
    return HEADER + html_text + FOOTER


def delete_build_folder(folder):
    shutil.rmtree("/folder_name", ignore_errors=True)


def create_site(path):

    delete_build_folder(f"{path}/{OUTPUT_FOLDER}")

    for notes_file in glob.glob("*.md", root_dir=path):
        with open(f"{path}/{notes_file}") as f:
            content = f.read()
            html = markdown.markdown(content, extensions=[CoolWikilinkExtension()])
            finished = add_header_and_footer(html)
            notes_file_name = modify_name(notes_file)
            folder_to_make = f"{path}/{OUTPUT_FOLDER}/{notes_file_name}"
            if not notes_file == "index.md":
                os.makedirs(folder_to_make)

            if notes_file == "index.md":
                folder_to_make = f"{path}/{OUTPUT_FOLDER}"
            with open(f"{folder_to_make}/index.html", "w") as h:
                h.write(finished)


if __name__ == "__main__":

    arguments = sys.argv
    path = arguments[-1]

    if not os.path.isdir(path):
        print("you need to give a directory!")
        exit

    create_site(path)

    print("... done!")
