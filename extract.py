import re, json

path = r'C:\Users\wildc\.claude\projects\C--Users-wildc-Runescape\a04e2cbe-3062-4812-a19e-378018354391\tool-results\artifact-6e29eee2-1786370031-a0a0.html'
with open(path, encoding='utf-8') as f:
    html = f.read()

# --- ITEMS ---
m = re.search(r'const ITEMS = \[(.*?)\n\];', html, re.S)
items_block = m.group(1)
row_re = re.compile(r'\["((?:[^"\\]|\\.)*)","((?:[^"\\]|\\.)*)","((?:[^"\\]|\\.)*)"\]')

def unesc(s):
    return s.replace('\\"', '"').replace("\\'", "'")

items = []
for region, name, level in row_re.findall(items_block):
    items.append({"region": unesc(region), "name": unesc(name), "level": unesc(level)})
print("items:", len(items))

# --- ICONS ---
m2 = re.search(r'const ICONS = \{(.*?)\n\};', html, re.S)
icons_block = m2.group(1)
icon_re = re.compile(r'"((?:[^"\\]|\\.)*)"\s*:\s*"(data:[^"]*)"')
icons = {}
for name, data in icon_re.findall(icons_block):
    icons[unesc(name)] = data
print("icons:", len(icons))

with open("items.json", "w", encoding="utf-8") as f:
    json.dump(items, f)
with open("icons.json", "w", encoding="utf-8") as f:
    json.dump(icons, f)

have = sum(1 for it in items if it["name"] in icons)
print("items with icon:", have, "/", len(items))
