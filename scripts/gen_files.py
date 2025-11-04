import mkdocs_gen_files

with open("README.md", "r") as f:
    content = f.read()

with mkdocs_gen_files.open("index.md", "w") as f:
    f.write(content)
