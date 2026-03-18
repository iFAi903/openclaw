import xml.etree.ElementTree as ET
tree = ET.parse("/Users/ifai_macpro/.openclaw/workspace/iFAi/workspace/xiaoyumao-news-web Refer/ProductHunt.xml")
root = tree.getroot()
ns = {'atom': 'http://www.w3.org/2005/Atom'}
for entry in root.findall('atom:entry', ns)[:2]:
    t = entry.find('atom:title', ns)
    s = entry.find('atom:summary', ns)
    if s is None:
        s = entry.find('atom:content', ns)
    print("Title:", t.text)
    print("Summary:", s.text.strip())
