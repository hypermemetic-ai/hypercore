#!/usr/bin/env python3
"""Generate "a card needs you" cue candidates — luxurious but simple.

The operator rejected the first (beepy sine) batch: wants a nice, professional,
luxurious-but-simple sound. These are warm glass/bell tones — inharmonic
partials for an expensive timbre, a soft bloom attack, a long graceful decay,
and a gentle reverb tail for space. One or two refined notes, never busy.
Pure-stdlib; re-run to tweak.

Play one:  paplay sounds/cue-glass.wav
"""
import math
import struct
import wave

SR = 44100
PEAK = 0.28  # gentle headroom

# Warm bell partials: (frequency ratio, amplitude, decay multiplier).
# Higher partials are quieter and fade faster — the warmth of a real bell.
BELL = [(1.0, 1.0, 1.00), (2.01, 0.50, 0.62), (2.96, 0.24, 0.42),
        (4.10, 0.11, 0.30), (5.43, 0.05, 0.22)]


def bell(freq, dur, t0=0.0, amp=1.0, tau=0.9, partials=BELL, attack=0.008):
    """One struck bell tone into a dur-second buffer, starting at t0."""
    n = int(SR * dur)
    buf = [0.0] * n
    a = int(SR * attack)
    s0 = int(SR * t0)
    for ratio, pa, dmult in partials:
        f = freq * ratio
        w = 2 * math.pi * f / SR
        for i in range(n - s0):
            env = math.exp(-(i / SR) / (tau * dmult))
            if i < a:
                env *= i / a
            buf[s0 + i] += amp * pa * env * math.sin(w * i)
    return buf


def reverb(dry, taps=((0.085, 0.30), (0.17, 0.17), (0.29, 0.09))):
    """A soft multi-tap tail for space — each copy delayed, attenuated, and
    gently low-passed for warmth. This is what reads as 'expensive'."""
    extra = int(SR * max(d for d, _ in taps)) + 1
    out = dry + [0.0] * extra
    for delay, gain in taps:
        d = int(SR * delay)
        lp = 0.0
        for i, s in enumerate(dry):
            lp += 0.45 * (s - lp)
            if i + d < len(out):
                out[i + d] += gain * lp
    return out


def finish(name, buf):
    peak = max((abs(x) for x in buf), default=1.0) or 1.0
    sc = PEAK / peak
    pcm = [int(max(-1.0, min(1.0, x * sc)) * 32767) for x in buf]
    with wave.open("sounds/" + name, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(b"".join(struct.pack("<h", s) for s in pcm))


def add(a, b):
    n = max(len(a), len(b))
    a = a + [0.0] * (n - len(a))
    b = b + [0.0] * (n - len(b))
    return [x + y for x, y in zip(a, b)]


# F5 — warm, not tinny
F5, C5, G5, A5 = 698.46, 523.25, 783.99, 880.0

# 1 — glass: a single warm bell note that blooms and fades. Simplest, calmest.
finish("cue-glass.wav", reverb(bell(F5, 1.7, tau=0.95)))

# 2 — fifth: two bell notes a perfect fifth apart, an unhurried, refined lift.
finish("cue-fifth.wav", reverb(add(
    bell(C5, 1.9, tau=0.85),
    bell(G5, 1.9, t0=0.18, amp=0.85, tau=0.95),
)))

# 3 — celesta: one bright music-box note with a faint detuned shimmer.
finish("cue-celesta.wav", reverb(add(
    bell(A5, 1.5, tau=0.70),
    bell(A5 * 1.003, 1.5, amp=0.4, tau=0.70),  # shimmer
)))

print("wrote sounds/cue-glass.wav, cue-fifth.wav, cue-celesta.wav")
