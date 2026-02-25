import os
import re

target_dir = "./src/apmodel"

pattern = r'Field\(default=(".*?"|\'.*?\'), kw_only=True, frozen=True\)'


def bulk_replace():
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)

                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()

                new_content = re.sub(pattern, r"\1", content)

                if content != new_content:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"置換完了: {path}")


if __name__ == "__main__":
    bulk_replace()
