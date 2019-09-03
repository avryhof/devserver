import re

from django import template
from django.forms.boundfield import BoundWidget
from django.utils.safestring import mark_safe

register = template.Library()


def auto_label(value):
    label_words = re.split(r"[\-_ ]+", value)
    label = " ".join(label_words).title()

    return label


def render_html(html):
    if isinstance(html, list):
        html = "".join(html)

    rendered_html = html

    return mark_safe(rendered_html)


def render_select(select_field):
    html = []
    html.append(
        '<select name="%s" id="%s" class="form-control" title="%s">'
        % (select_field.name, select_field.auto_id, select_field.help_text)
    )
    for subwidget in select_field.subwidgets:
        html.append(subwidget.tag())
    html.append("</select>")

    return render_html(html)


def render_text_input(text_input_field):
    html = []
    html.append(
        '<input type="text" name="%s" id="%s" class="form-control" title="%s">'
        % (text_input_field.name, text_input_field.auto_id, text_input_field.help_text)
    )

    return render_html(html)


@register.simple_tag
def checkbox_widget(form_field, name=False, id=False, id_suffix=False, label=False, help_text=False):
    # prescription.auto_refill 'auto_refill' 'auto_refill' prescription.rx_number
    html = []

    if isinstance(form_field, bool):
        if not label:
            label = auto_label(name)

        if id_suffix:
            id = "%s_%s" % (id, id_suffix)

        is_checked = form_field
        html.append('<div class="checkbox">')
        html.append('<label for="%s">' % id)
        html.append('<input type="checkbox" name="%s" id="%s" %s>' % (name, id, is_checked))
        html.append('<span class="checkmark"></span>')
        html.append('<span class="check-label">%s</span>' % label)
        html.append("</label>")
        html.append("</div>")

    else:
        is_checked = False
        if not isinstance(form_field, BoundWidget):
            is_checked = "checked" if form_field.value() else ""
            html.append('<div class="checkbox">')
            html.append('<label for="%s">' % form_field.id_for_label)
            html.append('<input type="checkbox" name="%s" id="%s" %s>' % (form_field.name, form_field.auto_id, is_checked))
            html.append('<span class="checkmark"></span>')
            html.append('<span class="check-label">%s</span>' % form_field.label)
            html.append("</label>")
            html.append("</div>")

        else:
            is_checked = 'checked="checked"' if form_field.data.get("selected") else ""
            html.append('<div class="checkbox">')
            html.append('<label for="%s">' % form_field.id_for_label)
            html.append(
                '<input type="checkbox" name="%s" id="%s" %s>'
                % (form_field.data.get("name"), form_field.data.get("attrs").get("id"), is_checked)
            )
            html.append('<span class="checkmark"></span>')
            html.append('<span class="check-label">%s</span>' % form_field.choice_label)
            html.append("</label>")
            html.append("</div>")

    return render_html(html)


@register.simple_tag
def radio_widget(form_field):
    html = []

    is_checked = False
    if not isinstance(form_field, BoundWidget):
        is_checked = "checked" if form_field.value() else ""
        html.append('<div class="radio">')
        html.append('<label for="%s">' % form_field.id_for_label)
        html.append(
            '<input type="radio" name="%s" id="%s" value="%s" %s>'
            % (form_field.name, form_field.auto_id, form_field.data.get("value"), is_checked)
        )
        html.append('<span class="checkmark"><span class="check-label">%s</span></span>' % form_field.choice_label)
        html.append("</label>")
        html.append("</div>")

    else:
        is_checked = 'checked="checked"' if form_field.data.get("selected") else ""
        html.append('<div class="radio">')
        html.append('<label for="%s">' % form_field.id_for_label)
        html.append(
            '<input type="radio" name="%s" id="%s" value="%s" %s>'
            % (
                form_field.data.get("name"),
                form_field.data.get("attrs").get("id"),
                form_field.data.get("value"),
                is_checked,
            )
        )
        html.append('<span class="checkmark"><span class="check-label">%s</span></span>' % form_field.choice_label)
        html.append("</label>")
        html.append("</div>")

    return render_html(html)


@register.simple_tag
def radio_select(form_field):
    html = []

    html.append('<label for="%s">%s</label>' % (form_field.id_for_label, form_field.label))
    html.append('<div id="id_%s">' % form_field.name)

    for subwidget in form_field.subwidgets:
        html.append(radio_widget(subwidget))

    html.append("</div>")

    return render_html(html)


# @register.simple_tag
# def form(form):
