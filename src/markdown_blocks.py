from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    if block.startswith(r"```"):
        return BlockType.CODE
    elif block.startswith(r">"):
        return BlockType.QUOTE
    elif block.startswith(r"- "):
        return BlockType.UNORDERED_LIST
    elif block.startswith(r"1."):
        return BlockType.ORDERED_LIST
    elif re.findall(r"^#{1,6}", block):
        return BlockType.HEADING
    else:
        return BlockType.PARAGRAPH
