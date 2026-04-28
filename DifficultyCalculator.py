import sys
from collections import defaultdict, deque
import math

# =========================
# DIFFICULTY
# =========================
class DifficultyCalculator:
    def __init__(self, notes, timing, resolution):
        self.raw_notes = notes
        self.timing = timing
        self.resolution = resolution
        self.notes = [(timing.tick_to_seconds(t), lane) for t, lane in notes]

    
    # -------------------------
    # HOPO / STRUM
    # -------------------------
    def classify_notes(self):
        classified = []

        HOPO_THRESHOLD = self.resolution / 3

        prev_tick = None
        prev_lane = None

        for tick, lane in self.raw_notes:
            note_type = "STRUM"

            if prev_tick is not None:
                dt = tick - prev_tick
                if dt <= HOPO_THRESHOLD and lane != prev_lane:
                    note_type = "HOPO"

            classified.append((tick, lane, note_type))

            prev_tick = tick
            prev_lane = lane

        return classified

    def split_note_types(self):
        classified = self.classify_notes()

        hopo_notes = []
        strum_notes = []

        for tick, lane, note_type in classified:
            if note_type == "HOPO":
                hopo_notes.append((tick, lane))
            else:
                strum_notes.append((tick, lane))

        return hopo_notes, strum_notes
    
    # -------------------------
    # PATTERN DETECTION
    # -------------------------
    def detect_patterns(self):
        patterns = {
            "trill": 0,
            "zigzag": 0,
            "stream": 0,
            "chord_stream": 0
        }

        window = deque(maxlen=6)

        grouped = defaultdict(list)
        for t, lane in self.raw_notes:
            grouped[t].append(lane)

        for i, (t, lane) in enumerate(self.raw_notes):
            window.append((t, lane))

            if len(window) < 4:
                continue

            lanes = [l for _, l in window]

            # TRILL (A-B-A-B)
            if len(set(lanes)) == 2:
                if lanes == [lanes[0], lanes[1], lanes[0], lanes[1]]:
                    patterns["trill"] += 1

            # JUMPS
            if len(set(lanes)) >= 3:
                diffs = [abs(lanes[i] - lanes[i - 1]) for i in range(1, len(lanes))]
                if all(d >= 2 for d in diffs):
                    patterns["zigzag"] += 1

            # STREAM (consistent fast notes)
            times = [t for t, _ in window]
            intervals = [times[i] - times[i - 1] for i in range(1, len(times))]

            if max(intervals) - min(intervals) < self.resolution * 0.05:
                patterns["stream"] += 1

        # chord stream
        for notes in grouped.values():
            if len(notes) >= 2:
                patterns["chord_stream"] += 1

        return patterns

    # -------------------------
    # STRAIN
    # -------------------------
    def compute_strain(self):
        classified = self.classify_notes()
        patterns = self.detect_patterns()

        prev_time = None
        prev_lane = None

        strain = 0
        strains = []

        for tick, lane, note_type in classified:
            time = self.timing.tick_to_seconds(tick)

            if prev_time is None:
                prev_time = time
                prev_lane = lane
                continue

            dt = time - prev_time
            if dt <= 0:
                continue

            strain *= 0.9 ** dt

            # base difficulty
            base = 1.3 if note_type == "STRUM" else 0.6

            # speed
            strain += base * (1 / dt)

            # movement
            movement = abs(lane - prev_lane)
            strain += movement * 0.25

            strains.append(strain)

            prev_time = time
            prev_lane = lane

        return strains, patterns

    # -------------------------
    # FINAL STARS
    # -------------------------
    def compute_stars(self):
        strains, patterns = self.compute_strain()

        if not strains:
          return 0, patterns

    # --- Clamp extreme strain values ---
        strains = [min(s, 50) for s in strains]

    # --- Take top peaks but fewer ---
        strains.sort(reverse=True)
        top = strains[:100]

    # --- Average instead of sum (BIG FIX) ---
        avg_strain = sum(top) / len(top)

    # --- Normalize by chart length ---
        length_factor = math.log(len(self.raw_notes) + 1, 10)

        base_difficulty = avg_strain / (8 + length_factor)

    # --- Pattern bonuses (heavily nerfed) ---
        pattern_bonus = (
        patterns["trill"] * 0.02 +
        patterns["zigzag"] * 0.03 +
        patterns["stream"] * 0.015 +
        patterns["chord_stream"] * 0.02
    )

    # --- Final scaling (compressed curve) ---
        stars = base_difficulty * 0.6 + pattern_bonus

    # soft cap curve (prevents 10 spam)
        stars = 10 * (stars / (stars + 5))

        return stars, patterns
    def compute_stars_for_notes(self, note_subset):
        if not note_subset:
            return 0, {}

        temp_calc = DifficultyCalculator(note_subset, self.timing, self.resolution)
        return temp_calc.compute_stars()