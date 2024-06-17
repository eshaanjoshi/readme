import markdown
from django import template

register = template.Library()

def create_md(source):
    #return source
    return markdown.Markdown(extensions=["fenced_code"]).convert(source)

register.filter("create_md", create_md)