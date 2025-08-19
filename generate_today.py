import datetime
import xml.etree.ElementTree as ET

# Load the full XML
tree = ET.parse("morneve.xml")
root = tree.getroot()

# Today’s date in MMDD format
today_id = datetime.datetime.utcnow().strftime("%m%d")

# Find morning and evening items
morning_item = root.find(f".//item[@id='{today_id}M']")
evening_item = root.find(f".//item[@id='{today_id}E']")

def build_rss(item, label):
    if item is not None:
        title = item.find("title").text
        desc = item.find("description").text
    else:
        title = f"{label} not found"
        desc = "No devotional available."

    return f"""<?xml version="1.0"?>
<rss version="2.0">
  <channel>
    <title>Spurgeon {label}</title>
    <link>https://github.com/Red-Beard08/morning-evening</link>
    <description>Daily devotional ({label})</description>
    <item>
      <title>{title}</title>
      <description>{desc}</description>
      <guid>{today_id}{label[0]}</guid>
      <pubDate>{datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}</pubDate>
    </item>
  </channel>
</rss>
"""

# Write morning
with open("today-morning.xml", "w", encoding="utf-8") as f:
    f.write(build_rss(morning_item, "Morning"))

# Write evening
with open("today-evening.xml", "w", encoding="utf-8") as f:
    f.write(build_rss(evening_item, "Evening"))
