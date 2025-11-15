from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
import textnode
import re


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise Exception("unknown text type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for n in old_nodes:
        if not n.text_type == TextType.PLAIN:
            new_nodes.append(n)
            continue
        text = n.text
        text = text.split(delimiter)
        if len(text) % 2 == 0:
            raise Exception("missing closing delimiter")

        sub_nodes = []
        for idx, t in enumerate(text):
            if idx % 2 == 0:
                sub_nodes.append(TextNode(t, TextType.PLAIN))
                continue
            sub_nodes.append(TextNode(t, text_type))
        new_nodes.extend((sub_nodes))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for n in old_nodes:
        if not n.text_type == TextType.PLAIN:
            new_nodes.append(n)
            continue
        text = n.text
        images = extract_markdown_images(text)
        if len(images) == 0:
            new_nodes.append((n))
            continue
        sub_nodes = []
        for image_alt, image_link in images:
            a, text = text.split(f"![{image_alt}]({image_link})", 1)
            sub_nodes.append(TextNode(a, TextType.PLAIN))
            sub_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
        new_nodes.extend((sub_nodes))
        if text:
            new_nodes.append((TextNode(text, TextType.PLAIN)))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for n in old_nodes:
        if not n.text_type == TextType.PLAIN:
            new_nodes.append(n)
            continue
        text = n.text
        links = extract_markdown_links(text)
        if len(links) == 0:
            new_nodes.append((n))
            continue
        sub_nodes = []
        for link_alt, link_link in links:
            a, text = text.split(f"[{link_alt}]({link_link})", 1)
            sub_nodes.append(TextNode(a, TextType.PLAIN))
            sub_nodes.append(TextNode(link_alt, TextType.LINK, link_link))
        new_nodes.extend((sub_nodes))
        if text:
            new_nodes.append((TextNode(text, TextType.PLAIN)))
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    return nodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [i.strip() for i in blocks if i]
    return blocks
