import os

favicon_tag = '<link rel="icon" type="image/png" href="sanokulov_favicon.png" sizes="32x32">\n'

def update_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if any(favicon_tag.strip() in line for line in lines):
        print(f"✔ Already updated: {filepath}")
        return

    for i, line in enumerate(lines):
        if '<head>' in line.lower():
            lines.insert(i + 1, '  ' + favicon_tag)
            break

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"✅ Updated: {filepath}")

def process_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.html'):
                update_html_file(os.path.join(root, file))

if __name__ == "__main__":
    website_folder = '.'  # current directory
    process_folder(website_folder)
