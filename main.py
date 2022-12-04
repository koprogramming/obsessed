import glob
import os
import sys

import markdown

OUTPUT_FOLDER = "build"


def get_markdown_files(path):

    for notes_file in glob.glob("*.md", root_dir=path):
        with open(f"{path}/{notes_file}") as f:
            content = f.read()
            html = markdown.markdown(content)

            with open(f"{path}/{OUTPUT_FOLDER}/{notes_file[:-3]}.html", "w") as h:
                h.write(html)


if __name__ == "__main__":

    arguments = sys.argv
    path = arguments[-1]

    if not os.path.isdir(path):
        print("you need to give a directory!")
        exit

    get_markdown_files(path)

    print("... done!")
