import os

def list_po():
    files = []
    for _, _, filesname in os.walk("po"):
        for file  in filesname:
            if file.endswith(".po"):
                files.append(file.strip(".po"))
    return files
    

with open("LINGUAS", "w") as file:
    po = "\n".join(list_po())
    file.write(po)

