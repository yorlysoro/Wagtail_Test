from wagtail.core import blocks
        
class RichtextBlock(blocks.RichTextBlock):

    class Meta:
        template = "home/richtext_block.html"
        icon = "doc-full"
        label = "RichText"