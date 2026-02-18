import os
import re

# 📂 Current folder
FOLDER = os.getcwd()

def clean_filename(name):
    """Clean unwanted characters and spaces"""
    name = name.replace("'", "")
    name = name.replace(":", "")
    name = name.replace("?", "")
    return name.strip()

def main():
    files = [f for f in os.listdir(FOLDER) if f.lower().endswith(".m4a")]
    files.sort()

    chapter_counter = 1

    for file in files:
        original_path = os.path.join(FOLDER, file)
        lower_name = file.lower()

        # 🎬 Opening Credits
        if "opening credits" in lower_name:
            new_name = "Opening_Credits.m4a"

        # 🎬 End Credits
        elif "end credits" in lower_name:
            new_name = "End_Credits.m4a"

        # 📖 Chapter Files
        else:
            new_name = f"Chapter_{chapter_counter:02d}.m4a"
            chapter_counter += 1

        new_path = os.path.join(FOLDER, new_name)

        print(f"🔄 Renaming: {file} → {new_name}")
        os.rename(original_path, new_path)

    print("\n✅ Done! Saare files Hogwarts level discipline me aa gaye.")

if __name__ == "__main__":
    main()
