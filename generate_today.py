import xml.etree.ElementTree as ET
from datetime import datetime
import os

SOURCE_FILE = "morneve.xml"

def format_rss(title, description, guid_suffix):
    pub_date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>{title}</title>
    <link>https://red-beard08.github.io/morning-evening/</link>
    <description>{title} from Spurgeon’s Morning and Evening</description>
    <item>
      <title>{title}</title>
      <link>https://red-beard08.github.io/morning-evening/{guid_suffix}.xml</link>
      <description><![CDATA[{description}]]></description>
      <guid isPermaLink="false">{guid_suffix}</guid>
      <pubDate>{pub_date}</pubDate>
    </item>
  </channel>
</rss>"""

def get_today_entry():
    # Today’s month/day key
    today = datetime.utcnow()
    key = today.strftime("%m%d")

    tree = ET.parse(SOURCE_FILE)
    root = tree.getroot()

    morning_text = "Morning devotional not found."
    evening_text = "Evening devotional not found."

    for entry in root.findall("DEVOTION"):
        if entry.get("id") == key:  # example: <DEVOTION id="0820">
            morning = entry.find("MORNING")
            evening = entry.find("EVENING")
            if morning is not None:
                morning_text = "".join(morning.itertext()).strip()
            if evening is not None:
                evening_text = "".join(evening.itertext()).strip()
            break

    return morning_text, evening_text

if __name__ == "__main__":
    morning_text, evening_text = get_today_entry()

    with open("today-morning.xml", "w", encoding="utf-8") as f:
        f.write(format_rss("Spurgeon Morning", morning_text, datetime.utcnow().strftime("%m%dM")))

    with open("today-evening.xml", "w", encoding="utf-8") as f:
        f.write(format_rss("Spurgeon Evening", evening_text, datetime.utcnow().strftime("%m%dE")))
