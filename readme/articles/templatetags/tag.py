import markdown
from django import template
import re
register = template.Library()

def create_md(source):
    #return source
    return markdown.Markdown(extensions=["fenced_code"]).convert(source)

"""<div style="text-align: center; display: flex; justify-content: center; align-items: center; flex-direction: column;">
    <div style="margin-bottom: 10px;">CMU</div>
    <img src="/static/media/kgb.gif" alt="CMU KGB" style="width: 100%; max-width: 50px; height: auto;">
    <div style="margin-top: 10px;">KGB</div>
</div>\n\n"""

def add_img_folder(folder):
    def add_img(filename):
        #return f"<img src=\"/static/{folder}/{filename}\" width=500>"
        return f"<img src=\"/static/{folder}/{filename}\" style=\"width: 50%; margin-left: 25%; height: auto;\"><br>\n\n"
    return add_img

def replace_double_braces(arg, folder):
    pattern = r'\{\{([^}]*)\}\}'
    replace = add_img_folder(folder)
    modified_text = re.sub(pattern, lambda x: replace(x.group(1)), arg)
    return modified_text

register.filter("create_md", create_md)
register.filter("imgswitch", replace_double_braces)