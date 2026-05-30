import os
import pygame

class Chart:
    def __init__(self, folder_path):
        self.folder = folder_path
        self.track = None
        self.bg = None
        self.pv = None
        self.chart_file = None
        self.notes = []

        self.load()

    def load(self):
        self.track = self._find_file([".mp3", ".wav", ".ogg"])
        self.bg = self._load_image([".png", ".jpg", ".jpeg"])
        self.pv = self._find_file([".mp4"])
        self.chart_file = self._find_file([".txt"])

        if self.chart_file:
            self.notes = self._load_chart_txt()

    def _find_file(self, exts):
        for file in os.listdir(self.folder):
            for ext in exts:
                if file.endswith(ext):
                    return os.path.join(self.folder, file)
        return None

    def _load_image(self, exts):
        path = self._find_file(exts)
        if path:
            return pygame.image.load(path).convert_alpha()
        return None

    def _load_chart_txt(self):
        notes = []

        with open(self.chart_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                parts = line.split(",")

                if len(parts) >= 2:
                    time_ms = int(parts[0])
                    note_type = parts[1]

                    notes.append({
                        "time": time_ms,
                        "type": note_type
                    })

        return notes