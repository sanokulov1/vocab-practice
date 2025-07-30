import os

# Correct GA4 script URL
correct_line = '<script async src="https://www.googletagmanager.com/gtag/js?id=G-0MJFGRJFR5"></script>'

# Traverse through all .html files
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".html"):
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            modified = False

            # Fix incorrect relative GA script line
            if 'src="js?id=G-0MJFGRJFR5"' in content:
                content = content.replace('src="js?id=G-0MJFGRJFR5"', correct_line)
                modified = True

            # Handle cases where the entire wrong line may have been inserted
            elif 'js?id=G-0MJFGRJFR5' in content:
                # Remove that line and insert the correct one just before </head>
                lines = content.splitlines()
                lines = [line for line in lines if 'js?id=G-0MJFGRJFR5' not in line]
                for i, line in enumerate(lines):
                    if '</head>' in line:
                        lines.insert(i, correct_line)
                        modified = True
                        break
                content = '\n'.join(lines)

            if modified:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ Fixed GA4 script in: {file_path}")
            else:
                print(f"⏩ No fix needed in: {file_path}")
