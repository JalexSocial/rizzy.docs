"""Regenerates the API tables in the docs from the Rizzy source.

The Typed Attributes and Events pages list every `Hx` builder method and every `HtmxEvents`
constant. Those tables sit between marker comments and are generated from:

  - Rizzy/src/Rizzy.Htmx/HxAttributes.cs  (one row per HxAttributes method, from its XML summary)
  - Rizzy/src/Rizzy.Htmx/HtmxEvents.cs    (one row per constant, grouped by extension)

Run it after changing either file:

    python scripts/generate_api_tables.py              # rewrite the tables
    python scripts/generate_api_tables.py --check      # exit 1 if they are out of date

By default the Rizzy repository is expected next to this one (../Rizzy); pass --rizzy <path>
otherwise.
"""
import argparse
import pathlib
import re
import sys

DOCS = pathlib.Path(__file__).resolve().parent.parent / 'content' / 'docs' / 'htmx'

# HxAttributes methods that are not attributes, or are explained in the page text instead.
SKIP_METHODS = {'WithMetaCharacter', 'Inherited', 'Append', 'Attr'}
# A method belongs to the extension table when its summary names an extension like "(Sse)".
EXTENSION_TAG = re.compile(r'\((Sse|Ws|Multipart|Preload|Head|Prompt|Live|Pending|PTag|Targets|'
                           r'BrowserIndicator|Csp|HistoryCache)\)')
METHOD = re.compile(r'    /// <summary>((?:(?!</summary>)[\s\S])*?)</summary>\n'
                    r'(?:    ///[^\n]*\n)*'
                    r'    public HxAttributes (\w+)\(([^)]*(?:\)\[\][^)]*)?)\)')
CONSTANT = re.compile(r'public const string (\w+) = "([^"]+)";')
EXTENSION_CLASS = re.compile(
    r'/// <summary>Events of the <c>([\w-]+)</c> extension \(<see cref="HtmxExtension\.\w+"/>\)\.</summary>\n'
    r'    public static class (\w+)\n    \{(.*?)\n    \}', re.S)


def xml_to_markdown(doc):
    doc = re.sub(r'\s*///\s*', ' ', doc).strip()
    doc = re.sub(r'<c>(.*?)</c>', r'`\1`', doc)
    doc = re.sub(r'<see cref="HtmxExtension\.(\w+)"/>', r'\1', doc)
    doc = re.sub(r'<see cref="(?:\w+\.)?(\w+)(?:\([^"]*\))?"/>', r'`\1`', doc)
    doc = re.sub(r'<paramref name="(\w+)"/>', r'`\1`', doc)
    doc = doc.replace('<see langword="true"/>', '`true`').replace('<see langword="false"/>', '`false`')
    return doc.replace('&lt;', '<').replace('&gt;', '>').replace('|', '\\|')


def attribute_tables(source):
    rows = []
    for doc, name, params in METHOD.findall(source):
        if name not in SKIP_METHODS:
            rows.append((name, re.sub(r'\s+', ' ', params.strip()), xml_to_markdown(doc)))
    extension = [r for r in rows if EXTENSION_TAG.search(r[2])]
    core = [r for r in rows if r not in extension]

    def table(items):
        lines = ['| Method | Description |', '|---|---|']
        lines += [f'| `{name}({params})` | {doc} |' for name, params, doc in items]
        return '\n'.join(lines)

    return {'core-attributes': table(core), 'extension-attributes': table(extension)}


def event_tables(source):
    def table(items, prefix):
        lines = ['| Constant | Event |', '|---|---|']
        lines += [f'| `{prefix}{name}` | `{event}` |' for name, event in items if name != 'ProcessPrefix']
        return '\n'.join(lines)

    core = source[:source.index('    /// <summary>Events of the')]
    rizzy = source[source.index('public static class Rizzy'):]
    sections = '\n\n'.join(f'### {file}\n\n' + table(CONSTANT.findall(body), f'HtmxEvents.{cls}.')
                           for file, cls, body in EXTENSION_CLASS.findall(source))
    return {
        'core-events': table(CONSTANT.findall(core), 'HtmxEvents.'),
        'extension-events': sections,
        'rizzy-events': table(CONSTANT.findall(rizzy), 'HtmxEvents.Rizzy.'),
    }


def replace_blocks(text, blocks, page):
    for name, content in blocks.items():
        pattern = re.compile(rf'(<!-- BEGIN GENERATED: {name} -->\n).*?(\n<!-- END GENERATED: {name} -->)', re.S)
        if not pattern.search(text):
            sys.exit(f'{page}: missing markers for "{name}"')
        text = pattern.sub(lambda m: m.group(1) + content + m.group(2), text)
    return text


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--rizzy', default=str(pathlib.Path(__file__).resolve().parents[2] / 'Rizzy'),
                        help='path to the Rizzy repository (default: ../Rizzy)')
    parser.add_argument('--check', action='store_true', help='exit 1 if the pages are out of date')
    args = parser.parse_args()

    htmx = pathlib.Path(args.rizzy) / 'src' / 'Rizzy.Htmx'
    pages = {
        DOCS / 'attributes.md': attribute_tables((htmx / 'HxAttributes.cs').read_text(encoding='utf-8')),
        DOCS / 'events.md': event_tables((htmx / 'HtmxEvents.cs').read_text(encoding='utf-8')),
    }

    stale = []
    for page, blocks in pages.items():
        current = page.read_text(encoding='utf-8')
        updated = replace_blocks(current, blocks, page.name)
        if updated != current:
            stale.append(page.name)
            if not args.check:
                page.write_text(updated, encoding='utf-8', newline='\n')

    if args.check and stale:
        sys.exit('Out of date: ' + ', '.join(stale) + ' (run python scripts/generate_api_tables.py)')
    print('Updated: ' + ', '.join(stale) if stale else 'API tables are up to date.')


if __name__ == '__main__':
    main()
