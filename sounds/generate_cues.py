#!/usr/bin/env python3
"""Generate gentle "a card needs you" cue candidates as 16-bit PCM WAVs.

Three soft, clear bell-like candidates for the hyper action cue (work card
"hyper: a sound cue when a card needs you", operator picked option 3 —
generate candidates to play and pick). Pure-stdlib; re-run to tweak.

Play one:  paplay sounds/cue-1-rising.wav
"""
import math
import struct
import wave

SR = 44100
PEAK = 0.26  # gentle — well below clipping


def tone(freq, dur, t0, amp=1.0, harmonics=(1.0, 0.35, 0.12), tau=0.18):
    """A soft bell tone: fundamental + a couple of decaying harmonics, with a
    short attack to kill clicks and an exponential decay for a chime feel.
    Returns (start_sample, [float samples])."""
    n = int(SR * dur)
    out = []
    attack = int(SR * 0.006)
    for i in range(n):
        t = i / SR
        env = math.exp(-t / tau)
        if i < attack:
            env *= i / attack
        s = sum(h * math.sin(2 * math.pi * freq * k * t)
                for k, h in enumerate(harmonics, start=1))
        out.append(amp * env * s)
    return int(SR * t0), out


def mix(layers, total_dur):
    buf = [0.0] * int(SR * total_dur)
    for start, samples in layers:
        for i, s in enumerate(samples):
            j = start + i
            if 0 <= j < len(buf):
                buf[j] += s
    peak = max((abs(x) for x in buf), default=1.0) or 1.0
    scale = PEAK / peak
    return [int(max(-1.0, min(1.0, x * scale)) * 32767) for x in buf]


def save(name, samples):
    with wave.open("sounds/" + name, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(b"".join(struct.pack("<h", s) for s in samples))


# C5, E5, G5, A5
C5, E5, G5, A5 = 523.25, 659.25, 783.99, 880.0

# 1 — rising two-note chime: a calm "ready" lift
save("cue-1-rising.wav", mix([
    tone(C5, 0.5, 0.00, tau=0.16),
    tone(E5, 0.7, 0.13, tau=0.22),
], 0.85))

# 2 — single soft mallet: one warm, clear note that fades
save("cue-2-mallet.wav", mix([
    tone(A5, 0.9, 0.00, harmonics=(1.0, 0.25, 0.06), tau=0.30),
], 0.95))

# 3 — gentle arpeggio: three light notes, unobtrusive
save("cue-3-arp.wav", mix([
    tone(C5, 0.45, 0.00, tau=0.14),
    tone(E5, 0.45, 0.10, tau=0.14),
    tone(G5, 0.7, 0.20, tau=0.22),
], 0.95))

print("wrote sounds/cue-1-rising.wav, cue-2-mallet.wav, cue-3-arp.wav")
