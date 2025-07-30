import os
import re
from bs4 import BeautifulSoup

def update_google_analytics_code(folder_path, new_measurement_id):
    """
    Updates Google Analytics code in all HTML files within a specified folder.
    It removes existing GA/GTM scripts and inserts the new GA4 snippet.

    Args:
        folder_path (str): The path to the folder containing HTML files.
        new_measurement_id (str): The new Google Analytics 4 Measurement ID (e.g., 'G-XWGHZ98G08').
    """

    # The new GA4 code snippet to be inserted
    new_ga4_snippet = f"""<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={new_measurement_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{new_measurement_id}');
</script>"""

    # Regex patterns to find and remove old Google Analytics / Google Tag Manager scripts
    # This pattern tries to catch common gtag.js and analytics.js snippets, and GTM snippets.
    # It's designed to be broad but might need adjustments for highly unusual existing setups.
    ga_patterns = [
        re.compile(r'<!--\s*Google Analytics\s*-->.*?<!--\s*End Google Analytics\s*-->', re.DOTALL | re.IGNORECASE),
        re.compile(r'<!--\s*Global site tag \(gtag\.js\)\s*-->.*?<\/script>', re.DOTALL | re.IGNORECASE),
        re.compile(r'<script[^>]*src=["\']https:\/\/www\.googletagmanager\.com\/(gtag|analytics|gtm)\.js\?[^"\']*["\'][^>]*>.*?<\/script>', re.DOTALL | re.IGNORECASE),
        re.compile(r'<script[^>]*>\s*\(function\(i,s,o,g,r,a,m\).*?<\/script>', re.DOTALL | re.IGNORECASE), # Universal Analytics (analytics.js)
        re.compile(r'<script[^>]*>\s*window\.dataLayer\s*=\s*window\.dataLayer\s*\|\|\s*\[\];.*?gtag\(\s*\'config\'.*?<\/script>', re.DOTALL | re.IGNORECASE) # gtag.js block
    ]

    for filename in os.listdir(folder_path):
        if filename.endswith(".html"):
            filepath = os.path.join(folder_path, filename)
            print(f"Processing: {filepath}")

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 1. Remove existing GA/GTM code using regex
                modified_content = content
                for pattern in ga_patterns:
                    modified_content = pattern.sub('', modified_content)

                # 2. Use BeautifulSoup to parse and insert the new snippet after <head>
                soup = BeautifulSoup(modified_content, 'html.parser')
                head_tag = soup.find('head')

                if head_tag:
                    # Remove any leftover script tags that might have been missed by regex
                    # This is a safety net for scripts that might not match the regex exactly
                    for script in head_tag.find_all('script', src=re.compile(r'googletagmanager\.com\/(gtag|analytics|gtm)\.js')):
                        script.decompose() # Remove the script tag

                    # Remove any inline GA/GTM scripts that might have been missed
                    for script in head_tag.find_all('script'):
                        if script.string and ('dataLayer' in script.string or 'gtag' in script.string or 'ga(' in script.string):
                            script.decompose()

                    # Insert the new GA4 snippet
                    # BeautifulSoup will automatically handle proper HTML escaping for the script tags
                    head_tag.insert(len(head_tag.contents), BeautifulSoup(new_ga4_snippet, 'html.parser'))
                    
                    # Convert back to string
                    updated_html = str(soup)

                    # Write the modified content back to the file
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(updated_html)
                    print(f"Successfully updated: {filename}")
                else:
                    print(f"Warning: No <head> tag found in {filename}. Skipping GA insertion.")

            except Exception as e:
                print(f"Error processing {filename}: {e}")

# --- Configuration ---
# IMPORTANT: Replace 'path/to/your/html/folder' with the actual path to your HTML files
HTML_FOLDER_PATH = 'C:/Users/hpenv/vocab-practice' 
NEW_GA4_MEASUREMENT_ID = 'G-XWGHZ98G08' # This is the new ID from your Google Analytics setup

# --- Run the script ---
if __name__ == "__main__":
    if HTML_FOLDER_PATH == 'path/to/your/html/folder':
        print("ERROR: Please update 'HTML_FOLDER_PATH' in the script with the actual path to your HTML folder.")
    else:
        update_google_analytics_code(HTML_FOLDER_PATH, NEW_GA4_MEASUREMENT_ID)
        print("\nAutomation complete. Please check your HTML files and test your website.")
        print("Remember to clear your browser cache and hard refresh your pages to see the changes.")

