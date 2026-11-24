#!/usr/bin/env python3
"""news-23 b113 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import hashlib
import os
import struct
import sys
import zlib

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
MIN_BYTES = 10_000
MAX_BYTES = 1_048_576


def fail(msg):
    print(f"error: {msg}", file=sys.stderr)
    return 1


def validate_png(data):
    """Parse the PNG header manually (struct): signature + IHDR + chunk walk."""
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return "bad PNG signature"
    if len(data) < 33:
        return "file too short for IHDR"
    # First chunk must be a 13-byte IHDR.
    (length,) = struct.unpack(">I", data[8:12])
    if data[12:16] != b"IHDR" or length != 13:
        return "first chunk is not a 13-byte IHDR"
    (width, height, depth, ctype, comp, filt, inter) = struct.unpack(
        ">IIBBBBB", data[16:29])
    if (width, height) != (1024, 1024):
        return f"bad dimensions {width}x{height}, want 1024x1024"
    if depth != 8 or ctype not in (2, 6):
        return f"bad bit depth {depth} / colour type {ctype}"
    if comp != 0 or filt != 0 or inter != 0:
        return "bad compression/filter/interlace byte"
    ihdr_crc = zlib.crc32(b"IHDR" + data[16:29]) & 0xFFFFFFFF
    (stored_crc,) = struct.unpack(">I", data[29:33])
    if ihdr_crc != stored_crc:
        return "IHDR CRC mismatch"
    # Chunk walk: every chunk CRC must match; IDAT payload non-empty;
    # IEND must be the last 0-byte chunk with no trailing data.
    # Chunk layout: 4-byte big-endian length + 4-byte type + body + 4-byte CRC.
    pos = 8
    idat_total = 0
    saw_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            return "truncated chunk header"
        (clen,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        if pos + 12 + clen > len(data):
            return f"truncated chunk {ctype!r}"
        body = data[pos + 8:pos + 8 + clen]
        (crc,) = struct.unpack(">I", data[pos + 8 + clen:pos + 12 + clen])
        if zlib.crc32(ctype + body) & 0xFFFFFFFF != crc:
            return f"CRC mismatch in chunk {ctype!r}"
        if ctype == b"IDAT":
            if clen == 0:
                return "empty IDAT chunk"
            idat_total += clen
        if ctype == b"IEND":
            if clen != 0:
                return "IEND chunk is not empty"
            if pos + 12 + clen != len(data):
                return "trailing data after IEND"
            saw_iend = True
            break
        pos += 12 + clen
    if not saw_iend:
        return "missing IEND chunk"
    if idat_total < 1000:
        return "IDAT payload suspiciously small"
    return None


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    repo = os.path.dirname(os.path.abspath(__file__))
    if out_dir_abs == repo or out_dir_abs.startswith(repo + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR must be outside the repo")
    if os.path.exists(out_dir_abs) and not os.path.isdir(out_dir_abs):
        return fail("MAKEFUN_OUTPUT_DIR exists and is not a directory")
    try:
        with open(SRC, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        return fail(f"cannot read source entry.png: {exc}")
    if len(data) < MIN_BYTES:
        return fail(f"entry.png too small: {len(data)} bytes")
    if len(data) > MAX_BYTES:
        return fail(f"entry.png too big: {len(data)} bytes")
    err = validate_png(data)
    if err:
        return fail(err)
    out_path = os.path.join(out_dir_abs, "entry.png")
    if os.path.abspath(out_path) == os.path.abspath(SRC):
        return fail("output would overwrite the source")
    os.makedirs(out_dir_abs, exist_ok=True)
    with open(out_path, "wb") as fh:
        fh.write(data)
    with open(out_path, "rb") as fh:
        back = fh.read()
    if back != data:
        return fail("output does not match source byte-for-byte")
    print(f"wrote {out_path} ({len(data)} bytes, "
          f"sha256 {hashlib.sha256(data).hexdigest()})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
