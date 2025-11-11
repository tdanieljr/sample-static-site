class HTMLNode:
    def __init__(self, tag=None, children=None, value=None, props=None) -> None:
        self.tag = tag
        self.children = children
        self.value = value
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        return "".join(f' {k}="{v}"' for k, v in self.props.items())

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag},{self.children},{self.value},{self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None) -> None:
        super().__init__(tag=tag, children=None, value=value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError("leaf must have value")
        if not self.tag:
            return f"{self.value}"

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag=tag, children=children, value=None, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("parent must have tag")
        if not self.children:
            raise ValueError("Parent must have childern")

        return f"<{self.tag}{self.props_to_html()}>{''.join(i.to_html() for i in self.children)}</{self.tag}>"
