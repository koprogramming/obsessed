from utils import modify_name, to_html


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
        self.outboud_links = []
        self.inbound_links = []
        # self.content_html = ""

    def __repr__(self) -> str:
        return f"<note object '{self.title}' >"

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

    def get_folder_path(self, output_folder):
        if self.title == "index":
            return f"{self.root_dir}/{output_folder}"
        return f"{self.root_dir}/{output_folder}/{self.output_folder_name}"

    def add_header_and_footer(self, header, footer):
        self.content_html = header + self.content_html + footer
