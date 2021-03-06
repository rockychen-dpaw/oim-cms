from django.conf import settings
from django.utils.html import format_html, format_html_join
from wagtail.wagtailcore import hooks


@hooks.register('insert_editor_js')
def enable_source():
    js_files = [
        'js/tinymce-textcolor-plugin.js',
    ]
    js_includes = format_html_join(
        '\n', '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files)
    )
    return js_includes + format_html(
        """
        <script>
            registerHalloPlugin('hallohtml');
            registerMCEPlugin('textcolor');
        </script>
        """
    )
