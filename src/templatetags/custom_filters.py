from django import template


register = template.Library()


@register.filter(name="placeholder")
def placeholder(value, token):
    """ Add placeholder attribute, esp. for form inputs and textareas """
    value.field.widget.attrs["placeholder"] = token
    return value


@register.filter(name="return_item")
def return_item(l, i):
    try:
        return l[i]
    except:
        return None
