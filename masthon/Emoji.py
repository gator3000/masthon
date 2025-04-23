class Emoji:
    __slots__ = ("shortcode", "url", "static_url", "visible_in_picker")
    def __init__(self, shortcode:str, url:str, static_url:str, visible_in_picker:bool):
        self.shortcode = shortcode
        self.url = url
        self.static_url = static_url
        self.visible_in_picker = visible_in_picker