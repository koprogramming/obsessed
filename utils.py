import markdown

from CoolWikilinksExtension import CoolWikilinkExtension


def to_html(md):
    return markdown.markdown(md, extensions=[CoolWikilinkExtension()])


def modify_name(notes_file_name: str):
    notes_file_name = notes_file_name.replace(" ", "_")
    if notes_file_name.endswith(".md"):
        notes_file_name = notes_file_name.removesuffix(".md")

    return notes_file_name
