# =========================
# TIMING
# =========================
class TimingEngine:
    def __init__(self, resolution, bpms):
        self.resolution = resolution
        self.bpms = bpms

    def tick_to_seconds(self, tick):
        total = 0
        prev_tick = 0
        bpm = self.bpms[0][1]

        for t, new_bpm in self.bpms:
            if tick < t:
                break
            dt = t - prev_tick
            total += (dt / self.resolution) * (60 / bpm)
            prev_tick = t
            bpm = new_bpm

        dt = tick - prev_tick
        total += (dt / self.resolution) * (60 / bpm)

        return total

