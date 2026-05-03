import glob

files = glob.glob("**/*.html", recursive=True)

for filepath in files:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        new_content = content.replace('href="/assets/css/main.css"', 'href="/assets/css/main.css?v=2"')
        
        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
    except Exception as e:
        pass

print("Cache busting query param added to ALL main.css links!")
