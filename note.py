from html.parser import HTMLParser

from utils import modify_name, to_html


class OutboudLinkParser(HTMLParser):
    def __init__(self, *, convert_charrefs: bool = ...) -> None:
        self.outbound_links = set([])
        super().__init__(convert_charrefs=convert_charrefs)

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr, data in attrs:
                if attr == "href":
                    self.outbound_links.add(data)


class Note:
    def __init__(self, filename: str, root_dir) -> None:
        self.filename = filename
        self.root_dir = root_dir.removesuffix("/")
        self.full_path = f"{root_dir}/{filename}"
        self.title = filename.removesuffix(".md")
        self.output_folder_name = f"{modify_name(self.filename)}"

        with open(f"{self.full_path}") as f:
            self.content_md = f"# {self.title} \n"
            self.content_md += f.read()

        self.content_html = to_html(self.content_md)
        self.parser = OutboudLinkParser()
        self.parser.feed(self.content_html)
        self.outbound_links = self.parser.outbound_links
        self.inbound_links = []

    def __repr__(self) -> str:
        return f"<note object '{self.title}' >"

    def to_link_path(self, folder_name):
        return f"/{folder_name}/"

    def update_inbound_links_from(self, other):
        if self.title == other.title:
            return
        if self.to_link_path(self.output_folder_name) in other.outbound_links:
            self.inbound_links.append(other)

    def is_in_folder(self):
        if self.title == "index":
            return False
        return True

    def is_special(self):
        if not self.is_in_folder():
            return True
        if self.title == "__left_hand_menu__":
            return True
        return False

    def add_inbound_links_to_content(self):
        links_to_add = [link for link in self.inbound_links if not link.is_special()]
        if links_to_add == []:
            return
        extra = "<div class='backlinks'>"
        extra += "\n<h2> Links to this page </h2>\n"
        for note in links_to_add:
            extra += f"\n<a class='backlink' href='/{note.output_folder_name}'>{note.title}</a>\n"
        extra += "\n</div>"

        self.content_html += extra

    def get_folder_path(self, output_folder):
        if self.title == "index":
            return f"{self.root_dir}/{output_folder}"
        return f"{self.root_dir}/{output_folder}/{self.output_folder_name}"

    def add_header_and_footer(self, header, footer):
        self.content_html = header + self.content_html + footer
