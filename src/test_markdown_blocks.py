import unittest
from markdown_blocks import block_to_block_type, BlockType


class TestSplit(unittest.TestCase):
    # TODO: Write a bunch more tests for this
    def test_split(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.PARAGRAPH, block_type)
        text = "```"

        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.CODE, block_type)
        text = "###"

        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.HEADING, block_type)
        text = "- "

        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.UNORDERED_LIST, block_type)
        text = "1."

        block_type = block_to_block_type(text)
        self.assertEqual(BlockType.ORDERED_LIST, block_type)


if __name__ == "__main__":
    unittest.main()
