import os

replacements = {
    'þ': 't',
    'Þ': 'T',
    'ª': 'S',
    'º': 's'
}

srt_files = [file for file in os.listdir('.') if file.endswith('.srt')]

for file in srt_files:
    with open(file, 'r', encoding='ansi') as f:
        content = f.read()
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    with open(file, 'w', encoding='ansi') as f:
        f.write(content)

print("OK.")
