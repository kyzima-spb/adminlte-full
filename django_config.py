import re


def static(_, filename):
    filename = re.sub(r'^(\'|")(.+)\1$', r'\1adminlte_full/\2\1', filename)
    return 'static', (filename,), {}


def adminlte_markup(name, *args, **kwargs):
    pattern = re.compile(r'^adminlte_markup\.([a-z0-9_.]+)$')
    name = pattern.sub(r'adminlte.render_\1', name)
    # return name, args, kwargs
    return name, (), {}


def bootstrap_breadcrumb(_, title='', url='', **kwargs):
    url_expr = re.match(r'("|\')?(.+)\1?', url)

    if url_expr:
        if url_expr.group(1):
            url = url_expr.group(2)
        else:
            url = '{{ %s }}' % url_expr.group(2)

    return 'breadcrumb', (title,), kwargs, url


def trans_or_blocktrans(_, s, *args, **kwargs):
    if not args and not kwargs:
        return 'trans', (s,)

    if kwargs:
        s = re.match(r'("|\')?(.+)\1+', s)
        placeholders = {name: '{{ %s }}' % name for name in kwargs.values()}
        return 'blocktrans', ('with',), kwargs, s.group(2) % placeholders

    raise RuntimeError(args)


def form_fields(_, form, *args, **kwargs):
    return 'crispy', (form,)


def replace_with_include(template):
    def f(_, **kwargs):
        if kwargs:
            return 'include', (f"'{template}'", 'with'), kwargs
        return 'include', (f"'{template}'",), {}
    return f


ENVIRONMENT_AUTOESCAPE = False
ENVIRONMENT_EXTENSIONS = ['jinja2.ext.i18n']
# ENVIRONMENT_EXTENSIONS = ['jinja_to_another.i18n']


GENERATOR_FUNCTIONS_MAPPER = {
    re.compile(r'(?:adminlte_markup\.)?sidebar_menu'): replace_with_include('adminlte_full/markup/sidebar_menu.html'),
    'adminlte_markup.navbar_menu': replace_with_include('adminlte_full/markup/navbar_menu.html'),
    'navbar_dropdown': replace_with_include('adminlte_full/markup/navbar_dropdown.html'),
    'adminlte_markup.navbar_search_form': replace_with_include('adminlte_full/markup/navbar_search_form.html'),
    'adminlte.create_url': 'url',
    'adminlte.static': static,
    # 'adminlte_markup.flash_messages': lambda *args: ('adminlte.render_flash_messages', (), {}),
    re.compile(r'^adminlte_markup\.([a-z0-9_.]+)$'): adminlte_markup,
    # 'adminlte_markup.navbar_search_form': adminlte_markup,
    'bootstrap.form_fields': form_fields,
    'bootstrap.breadcrumb': bootstrap_breadcrumb,
    '_': 'trans',
    'gettext': 'trans',
    'adminlte.gettext': trans_or_blocktrans,
}

GENERATOR_TEMPLATE_TAGS = {
    r'^crispy$': 'crispy_forms_tags',
    r'^adminlte\.gettext': 'i18n',
    r'^adminlte\.[a-z0-9_.]+$': 'adminlte_full',
    r'^adminlte_markup\.[a-z0-9_.]+$': 'adminlte_full',
    r'breadcrumb': 'adminlte_full',
    r'^(gravatar|if_true|humanize)$': 'adminlte_full',
    r'^(_|gettext|trans|blocktrans)$': 'i18n',
}
