# -*- coding: utf-8 -*-
import re
from bibtexparser.customization import convert_to_unicode


# ###############
# JINJA FILTERS #
# ###############

def ordinal(value):
    """ Cardinal to ordinal conversion for the edition field """
    try:
        digit = int(value)
    except:
        return value.split(' ')[0]

    if digit < 1:
        return digit

    if digit % 100 == 11 or digit % 100 == 12 or digit % 100 == 13:
        return value + 'th'
    elif digit % 10 == 3:
        return value + 'rd'
    elif digit % 10 == 2:
        return value + 'nd'
    elif digit % 10 == 1:
        return value + 'st'
    else:
        return value + 'th'


def keeponly(value, val, field='ENTRYTYPE'):
    """ Filter by BibTeX field """
    if isinstance(val, str):
        return [entry for entry in value
                if field in list(entry.keys()) and entry[field] == str(val)]
    elif isinstance(val, list):
        return [entry for entry in value
                if field in list(entry.keys()) and entry[field] in val]


def author_join(value, d=', ', last=', and ', two=' and '):
    """ Like join but for list of names (convenient authors list) """
    if len(value) == 1:
        return value[0]
    elif len(value) == 2:
        return value[0] + two + value[1]
    else:
        return d.join(value[:-1]) + last + value[-1]

def highlight_JNW(value):
    output = []
    if len(value)>1:
        for name in value:
            if "Jonathan" in name and "Washington" in name:
                outname = "<span class=\"pub-author-me\">" + name + "</span>"
            else:
                outname = name
            output.append(outname)
    else:
        output.append("")
    #print(output)
    return output


# ##############################
# BIBTEX PARSER CUSTOMIZATIONS #
# ##############################

def customizations(entry):
    entry = clear_empty(entry)
    entry = author(entry)
    entry = page_endash(entry)
    entry = convert_to_unicode(entry)
    entry = clean_latex(entry)

    return entry


def clear_empty(entry):
    """ Clear empty fields in entry """
    gen = (field for field in list(entry.keys()) if not entry[field])

    for field in gen:
        del entry[field]

    return entry


def author(entry):
    """ Convert author field to list """
    if 'author' in entry:
        entry['author'] = [name for name in entry['author'].replace('\n', ' ').replace('{', '').replace('}', '').split(' and ')
                           if name.strip()]
    #print(entry['author'])

    return entry


def page_endash(entry):
    """ Separate pages by an HTML endash (&ndash;) """
    if "pages" in entry:
        p = re.findall(r'\d+', entry["pages"])
        entry["pages"] = p[0] + '&ndash;' + p[-1]
    return entry


def clean_latex(entry, fields=['title', 'note']):
    """ Cleans up LaTeX markup from entries """
    # LaTeX markup regex
    italic = r'\\textit\{([^\}]*)\}'
    emph = r'\\emph\{([^\}]*)\}'
    bold = r'\\textbf\{([^\}]*)\}'
    hyperlink = r'\\url\{([^\}]*)\}'
    markup = r'\\[^\{]*\{([^\}]*)\}'

    for field in list(entry.keys()):
        if field != "bibTex":
            val = entry[field]

            try:
                val = re.sub(italic, r'<i>\g<1></i>', val)
                val = re.sub(emph, r'<i>\g<1></i>', val)
                val = re.sub(bold, r'<b>\g<1></b>', val)
                val = re.sub(hyperlink, r'<a href="\g<1>">\g<1></a>', val)
                val = re.sub(markup, r'\g<1>', val)
                val = re.sub(r'[\{\}]', '', val)
                entry[field] = val
            except:
                pass

    return entry
