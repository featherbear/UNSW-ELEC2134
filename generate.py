import os
import urllib.parse

rootDir = os.path.basename(os.getcwd())

def generateHTML(title, directories, files):
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Andrew Wong</title>
</head>
<body>

<h1>{title}</h1>
<ul>
{chr(10).join(f"<li><a href={urllib.parse.quote(path)}>[{path}]</a></li>" for path in directories)}
{chr(10).join(f"<li><a href={urllib.parse.quote(path)}>{path.split('.', 1)[0]}</a></li>" for path in files)}
</ul>

<hr>

<i>These notes were <a href="https://www.passbe.com/2019/08/01/bulk-export-onenote-2013-2016-pages-as-html/">generated</a> from OneNote.  
Sorry if it looks like a mess!</i>

<script async src="https://www.googletagmanager.com/gtag/js?id=UA-107434487-2"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag() {{
      dataLayer.push(arguments);
  }}
  gtag('js', new Date());

  gtag('config', 'UA-107434487-2');
</script>
</body>
</html>
"""


def process(directory="."):
    status = False
    path, dirs, files = next(os.walk(directory))

    outputDirs = []
    outputFiles = []

    for _path in sorted(dirs):
        if _path.endswith("_files") or not process(os.path.join(path, _path)):
            continue
        status = True
        outputDirs.append(_path)

    for _file in sorted(files):
        if not _file.lower().endswith("htm") and not _file.lower().endswith("html"):
            continue
        if _file.lower().endswith("index.html"):
            continue
        status = True
        outputFiles.append(_file)

    if status:
        if directory != ".":
            outputDirs.append("..")
            outputDirs.sort()
        with open(os.path.join(path, "index.html"), "w") as f:
            f.write(generateHTML(" > ".join(filter(lambda _: _, [rootDir, *directory[2:].split("/")])), outputDirs, outputFiles))

    return status


process()
