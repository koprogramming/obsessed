import glob
import os
import shutil
import sys
from typing import List

import markdown
from markdown.extensions.wikilinks import WikiLinkExtension

from CoolWikilinksExtension import CoolWikilinkExtension
from note import Note
from utils import modify_name, to_html

OUTPUT_FOLDER = "build"

HEADER = ""
FOOTER = ""


with open("./fragments/_foot.html") as f, open("./fragments/_head.html") as h:
    HEADER = h.read()
    FOOTER = f.read()


def add_header_and_footer(header, html_text, footer):
    """
    Adds a header and a footer
    """


def delete_build_folder(folder):
    shutil.rmtree(folder, ignore_errors=True)
    os.mkdir(folder)


def make_left_hand_menu(HEADER, list_of_links, folder):
    content = ""
    with open(f"{folder}/__left_hand_menu__.md") as f:
        content = to_html(f.read())

    content += list_of_links
    return HEADER.format(left_hand_menu=content)


def create_notes_list(notes):
    notes_list = "<div> <h2> All posts 👇 </h2>"
    for note in notes:
        if note.is_special():
            continue
        notes_list += (
            f"\n <p><a href='/{note.output_folder_name}'> {note.title} </a></p> \n"
        )
    notes_list += "\n</div>"
    return notes_list


def create_site(path):

    delete_build_folder(f"{path}/{OUTPUT_FOLDER}")
    for style_file in glob.glob("*.css", root_dir=path):
        fc = ""
        with open(f"{path}/{style_file}") as sf:
            fc = sf.read()
        with open(f"{path}/{OUTPUT_FOLDER}/{style_file}", "w") as f:
            f.write(fc)

    notes: List[Note] = []
    for notes_file in glob.glob("*.md", root_dir=path):
        notes.append(Note(notes_file, path))

    for note_a in notes:
        for note_b in notes:
            note_a.update_inbound_links_from(note_b)

    for note in notes:
        note.add_inbound_links_to_content()

    header = make_left_hand_menu(HEADER, create_notes_list(notes), path)

    for note in notes:
        folder_path = note.get_folder_path(OUTPUT_FOLDER)

        if note.is_in_folder():
            os.makedirs(folder_path)

        note.add_header_and_footer(header, FOOTER)
        with open(f"{folder_path}/index.html", "w") as h:
            h.write(note.content_html)


if __name__ == "__main__":

    arguments = sys.argv
    path = arguments[-1]

    if not os.path.isdir(path):
        print("you need to give a directory!")
        exit

    create_site(path)

    print("... done!")
