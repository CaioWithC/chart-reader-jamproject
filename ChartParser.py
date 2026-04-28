import re

# =========================
# PARSER
# =========================
class ChartParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.resolution = 192
        self.notes = []
        self.bpms = [(0, 120)]
        self.title = "Unknown"
        self.artist = "Unknown"

    def parse(self):
        section = None

        with open(self.filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                if line.startswith("[") and line.endswith("]"):
                    section = line[1:-1]
                    continue

                if section == "Song":
                    if "Resolution" in line:
                        self.resolution = int(re.findall(r'\d+', line)[0])

                if "Name" in line:
                    match = re.search(r'"(.+)"', line)
                    if match:
                        self.title = match.group(1)

                if "Artist" in line:
                    match = re.search(r'"(.+)"', line)
                    if match:
                        self.artist = match.group(1)       

                if section == "SyncTrack":
                    match = re.match(r"(\d+)\s*=\s*B\s*(\d+)", line)
                    if match:
                        tick = int(match.group(1))
                        bpm = int(match.group(2)) / 1000
                        self.bpms.append((tick, bpm))

                if section and "Single" in section:
                    match = re.match(r"(\d+)\s*=\s*N\s*(\d+)\s*(\d+)", line)
                    if match:
                        tick = int(match.group(1))
                        lane = int(match.group(2))
                        self.notes.append((tick, lane))

        self.notes.sort()
        self.bpms.sort()
        return self.notes
