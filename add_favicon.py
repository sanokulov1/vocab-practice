import os

FAVICON_LINE = '<link rel="icon" type="image/png" href="sanokulov_favicon.png" sizes="32x32">'
INSERT_AFTER_TAG = '<head>'

def update_favicon_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip files without a <head> tag
    if INSERT_AFTER_TAG not in content:
        return

    # Remove existing favicon lines
    lines = content.splitlines()
    new_lines = []
    favicon_inserted = False

    for line in lines:
        if 'rel="icon"' in line or 'rel=\'icon\'' in line:
            continue  # Skip existing favicon lines
        new_lines.append(line)
        if INSERT_AFTER_TAG in line and not favicon_inserted:
            new_lines.append('  ' + FAVICON_LINE)
            favicon_inserted = True

    new_content = '\n'.join(new_lines)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f'✅ Updated: {filepath}')


def fix_all_html_files(root_dir='.'):
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                full_path = os.path.join(root, file)
                update_favicon_in_file(full_path)

if __name__ == '__main__':
    fix_all_html_files()
