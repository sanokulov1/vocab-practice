import os

# GA4 tracking code (you can safely copy-paste this)
ga4_code = '''
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0MJFGRJFR5"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-0MJFGRJFR5');
</script>
'''.strip()

# Traverse all .html files in the current directory and subdirectories
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".html"):
            file_path = os.path.join(root, file)

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Skip files that already have this GA4 script
            if "G-0MJFGRJFR5" in content:
                print(f"⏩ Already has GA4: {file_path}")
                continue

            # Make sure </head> exists
            if "</head>" in content:
                new_content = content.replace("</head>", ga4_code + "\n</head>")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"✅ GA4 added: {file_path}")
            else:
                print(f"⚠️ Missing </head>: {file_path}")
