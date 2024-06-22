import markdown
from django import template
import re
register = template.Library()

def create_md(source):
    #return source
    return markdown.Markdown(extensions=["fenced_code"]).convert(source)

def add_img_folder(folder):
    def add_img(filename):
        return f"<img src=\"/static/{folder}/{filename}\" width=500>"
    return add_img

def replace_double_braces(arg, folder):
    pattern = r'\{\{([^}]*)\}\}'
    replace = add_img_folder(folder)
    modified_text = re.sub(pattern, lambda x: replace(x.group(1)), arg)
    return modified_text

register.filter("create_md", create_md)
register.filter("imgswitch", replace_double_braces)