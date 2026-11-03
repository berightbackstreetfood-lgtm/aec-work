#!/usr/bin/env python3
"""pr_check.py — kiểm PR cho repo công khai aec-work (chỉ Python stdlib).

Chạy từ bản TIN CẬY (main). Đọc PR như DỮ LIỆU qua git plumbing
(diff-tree, cat-file) — không checkout, không textconv, không filter.

Dùng: python3 -I pr_check.py --repo DIR --base <sha main> --head <sha PR>
      Thay đổi được so từ merge-base(base, head) tới head.

Log (repo công khai => log công khai với mọi tài khoản đã đăng nhập):
  KHÔNG in giá trị khớp, nội dung dòng, TÊN/ĐƯỜNG DẪN file của PR,
  thông báo git, hay thông điệp ngoại lệ. Chỉ in:
  file#<thứ tự>[<8 hex đầu sha256(đường dẫn)>] dòng <n>: <MÃ>
  Ngoại lệ: "QUEUE.md" là tên cố định trong code tin cậy.
  Owner tự đối chiếu: printf %s 'đường/dẫn' | sha256sum | cut -c1-8
Chính sách file: repo chỉ chứa VĂN BẢN UTF-8. File không đọc được dạng UTF-8
  (ảnh, PDF, nhị phân…) => báo đỏ FILE_NHI_PHAN_KHONG_CHO_PHEP (không thuộc phạm vi
  repo; không quét được nên không cho qua). File > 1 MB => FILE_QUA_LON_KHONG_QUET.
Mã thoát: 0 sạch · 1 có lỗi · 2 công cụ lỗi (coi như không đạt).
"""
import argparse
import fnmatch
import hashlib
import re
import subprocess
import sys
import unicodedata

MAX_BYTES = 1_000_000

# ---------- (3) tên file cấm ----------
FORBIDDEN_NAMES = [".env*", "*.pem", "id_rsa*", "*.key", "credentials*"]

# ---------- (2) mẫu nhạy cảm ----------
PATTERNS = [
    ("EMAIL", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")),
    ("KEY_ANTHROPIC", re.compile(r"sk-ant-[A-Za-z0-9_-]{8,}")),
    ("KEY_SK", re.compile(r"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}")),
    ("TOKEN_GITHUB", re.compile(r"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})")),
    ("KEY_AWS", re.compile(r"(?<![A-Z0-9])(?:AKIA|ASIA)[A-Z0-9]{16}(?![A-Z0-9])")),
    ("TOKEN_SLACK", re.compile(r"xox[abposr]-[A-Za-z0-9-]{10,}")),
    ("PRIVATE_KEY", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("PATH_HOME", re.compile(r"/home/[A-Za-z0-9._-]+")),
    ("PATH_WINUSER", re.compile(r"[A-Za-z]:\\+Users\\+[^\\\s\"'<>|]+", re.I)),
]
HEX_RE = re.compile(r"(?<![0-9A-Za-z])[0-9A-Fa-f]{32,}(?![0-9A-Za-z])")
B64_RE = re.compile(r"(?<![A-Za-z0-9+/_-])[A-Za-z0-9+/_-]{32,}={0,2}")
DRIVE_CTX_RE = re.compile(r"drive|docs\.google", re.I)
DRIVE_ID_RE = re.compile(r"(?<![A-Za-z0-9_-])[A-Za-z0-9_-]{25,44}(?![A-Za-z0-9_-])")
IBAN_RE = re.compile(r"(?<![A-Z0-9])[A-Z]{2}[0-9]{2}(?: ?[A-Z0-9]{4}){2,7}(?: ?[A-Z0-9]{1,3})?(?![A-Z0-9])")
# Nới có kiểm soát: hash git/sha256 = ĐÚNG 40 hoặc 64 hex, CHỮ THƯỜNG, và dòng có ngữ cảnh hash.
HASH_CTX_RE = re.compile(r"sha(?:1|256)?\b|sha256sum|\bcommit\b|/commit/|\buses:\s*\S+@", re.I)
URL_SPLIT_RE = re.compile(r"[/?&=#:]")

# ---------- (1) QUEUE.md ----------
QUEUE_FILE = "QUEUE.md"
QUEUE_SECTION = "## Việc hiện tại"
QUEUE_HEADER = ["ID", "Việc", "Người làm", "Trạng thái", "Cần ai duyệt", "Ghi chú"]
STATUS_RE = re.compile(r"^(ĐANG CHỜ|CHỜ \S.*|ĐANG LÀM(?: .*)?|XONG(?: .*)?|BLOCKED)$")


class ToolError(Exception):
    """Lỗi công cụ; chỉ mang MÃ, không mang dữ liệu."""


class Report:
    def __init__(self):
        self.errors = 0
        self.warnings = 0

    def error(self, label, line, code):
        self.errors += 1
        where = f"{label} dòng {line}" if line else label
        print(f"::error::{where}: {code}")

    def warn(self, label, code):
        self.warnings += 1
        print(f"::warning::{label}: {code}")


def label(idx, path):
    return f"file#{idx}[{hashlib.sha256(path.encode('utf-8', 'surrogateescape')).hexdigest()[:8]}]"


def git(repo, *args, code="GIT_LOI"):
    """git plumbing; stderr bị bỏ, lỗi đổi thành MÃ."""
    p = subprocess.run(
        ["git", "-c", "core.hooksPath=/dev/null", "-C", repo, *args],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        env={"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null",
             "GIT_TERMINAL_PROMPT": "0", "PATH": "/usr/bin:/bin:/usr/local/bin",
             "LC_ALL": "C"})
    if p.returncode != 0:
        raise ToolError(code)
    return p.stdout


def changed_entries(repo, base, head):
    """[(src_mode, dst_mode, dst_sha, status, path)] từ diff-tree (plumbing, -z)."""
    mb = git(repo, "merge-base", base, head, code="KHONG_CO_MERGE_BASE").decode().strip()
    out = git(repo, "diff-tree", "-r", "-z", "--no-renames", "--no-ext-diff",
              mb, head, code="DIFF_LOI")
    parts = out.split(b"\0")
    res, i = [], 0
    while i + 1 < len(parts):
        meta = parts[i].decode("ascii")
        if not meta.startswith(":"):
            raise ToolError("DIFF_DINH_DANG_LA")
        src_mode, dst_mode, _src_sha, dst_sha, status = meta[1:].split(" ")
        path = parts[i + 1].decode("utf-8", "surrogateescape")
        res.append((src_mode, dst_mode, dst_sha, status, path))
        i += 2
    return res


def mixed(s):
    return any(c.isdigit() for c in s) and any(c.isalpha() for c in s)


def b64_like(s):
    s = s.rstrip("=")
    return (any(c.isdigit() for c in s) and any(c.isupper() for c in s)
            and any(c.islower() for c in s))


def iban_ok(raw):
    s = raw.replace(" ", "")
    if not (15 <= len(s) <= 34):
        return False
    r = s[4:] + s[:4]
    return int("".join(str(int(c, 36)) for c in r)) % 97 == 1


def is_allowed_hash(tok, line):
    return (len(tok) in (40, 64) and tok == tok.lower()
            and HASH_CTX_RE.search(line) is not None)


def candidates(line):
    """Các chuỗi để thử hex/base64: từ thường giữ nguyên; URL tách theo / ? & = # :"""
    for word in line.split():
        if "://" in word:
            yield from (seg for seg in URL_SPLIT_RE.split(word) if seg)
        else:
            yield word


def scan_line(line):
    found = []
    for code, rx in PATTERNS:
        if rx.search(line):
            found.append(code)
    hex_hit = b64_hit = False
    for cand in candidates(line):
        for m in HEX_RE.finditer(cand):
            t = m.group()
            if mixed(t) and not is_allowed_hash(t, line):
                hex_hit = True
        for m in B64_RE.finditer(cand):
            t = m.group()
            if HEX_RE.fullmatch(t):
                continue  # chuỗi hex thuần đã xét ở trên
            if b64_like(t):
                b64_hit = True
    if hex_hit:
        found.append("LONG_HEX")
    if b64_hit:
        found.append("LONG_BASE64")
    if DRIVE_CTX_RE.search(line) and any(mixed(m.group()) and not is_allowed_hash(m.group(), line)
                                         for m in DRIVE_ID_RE.finditer(line)):
        found.append("DRIVE_ID")
    m = IBAN_RE.search(line)
    if m:
        found.append("IBAN" if iban_ok(m.group()) else "IBAN_NGHI")
    return list(dict.fromkeys(found))


def split_row(row):
    row = row.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|") and not row.endswith("\\|"):
        row = row[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", row)]


def check_queue(text, rep):
    lines = text.splitlines()
    try:
        start = next(i for i, l in enumerate(lines) if l.strip() == QUEUE_SECTION)
    except StopIteration:
        rep.error(QUEUE_FILE, 0, "QUEUE_THIEU_MUC_VIEC_HIEN_TAI")
        return
    i = start + 1
    while i < len(lines) and not lines[i].strip().startswith("|"):
        if lines[i].startswith("## "):
            break
        i += 1
    if i >= len(lines) or not lines[i].strip().startswith("|"):
        rep.error(QUEUE_FILE, start + 1, "QUEUE_THIEU_BANG")
        return
    if split_row(lines[i]) != QUEUE_HEADER:
        rep.error(QUEUE_FILE, i + 1, "QUEUE_TIEU_DE_SAI (cần: " + " | ".join(QUEUE_HEADER) + ")")
        return
    sep = i + 1
    if sep >= len(lines) or not re.fullmatch(r"\|?(\s*:?-{3,}:?\s*\|){5}\s*:?-{3,}:?\s*\|?", lines[sep].strip()):
        rep.error(QUEUE_FILE, sep + 1, "QUEUE_DONG_PHAN_CACH_SAI")
    seen = {}
    j = sep + 1
    while j < len(lines) and lines[j].strip().startswith("|"):
        n = j + 1
        cells = split_row(lines[j])
        if len(cells) != 6:
            rep.error(QUEUE_FILE, n, f"QUEUE_SO_COT_SAI ({len(cells)}/6)")
        else:
            if any(c == "" for c in cells):
                rep.error(QUEUE_FILE, n, "QUEUE_O_TRONG (ghi CẦN XÁC NHẬN hoặc —)")
            rid = cells[0]
            if rid in seen:
                rep.error(QUEUE_FILE, n, f"QUEUE_ID_TRUNG (trùng dòng {seen[rid]})")
            elif rid:
                seen[rid] = n
            if not STATUS_RE.match(cells[3]):
                rep.error(QUEUE_FILE, n, "QUEUE_TRANG_THAI_SAI (ĐANG CHỜ | CHỜ … | ĐANG LÀM… | XONG … | BLOCKED)")
        j += 1
    if not seen:
        rep.warn(QUEUE_FILE, "QUEUE_BANG_RONG")


def run(a):
    rep = Report()
    entries = changed_entries(a.repo, a.base, a.head)
    print(f"Số file thay đổi: {len(entries)}")
    for idx, (_sm, dmode, dsha, st, path) in enumerate(entries, 1):
        lb = label(idx, path)
        if path.startswith(".github/"):
            rep.warn(lb, "PR_SUA_CONG_CU_KIEM (không ảnh hưởng lần kiểm này; Owner đọc kỹ diff)")
        if st == "D":
            continue
        for code in scan_line(path):
            rep.error(lb, 0, "TEN_FILE_CHUA_" + code)
        name = path.rsplit("/", 1)[-1].lower()
        if any(fnmatch.fnmatch(name, p) for p in FORBIDDEN_NAMES):
            rep.error(lb, 0, "TEN_FILE_CAM")
            continue  # không đọc nội dung
        if dmode == "160000":
            rep.error(lb, 0, "SUBMODULE_KHONG_CHO_PHEP")
            continue
        size = int(git(a.repo, "cat-file", "-s", dsha, code="DOC_FILE_LOI").strip() or 0)
        if size > MAX_BYTES:
            rep.error(lb, 0, "FILE_QUA_LON_KHONG_QUET")
            continue
        data = git(a.repo, "cat-file", "blob", dsha, code="DOC_FILE_LOI")
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            rep.error(lb, 0, "FILE_NHI_PHAN_KHONG_CHO_PHEP")
            continue
        text = unicodedata.normalize("NFC", text)
        for n, line in enumerate(text.splitlines(), 1):
            for code in scan_line(line):
                rep.error(lb, n, code)
    # QUEUE.md luôn kiểm ở head
    try:
        q = git(a.repo, "cat-file", "blob", f"{a.head}:{QUEUE_FILE}", code="QUEUE_KHONG_TIM_THAY")
        check_queue(unicodedata.normalize("NFC", q.decode("utf-8")), rep)
    except ToolError as e:
        rep.error(QUEUE_FILE, 0, str(e))
    except UnicodeDecodeError:
        rep.error(QUEUE_FILE, 0, "QUEUE_KHONG_PHAI_UTF8")
    print(f"Kết quả: {rep.errors} lỗi, {rep.warnings} cảnh báo")
    return 1 if rep.errors else 0


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--head", required=True)
    try:
        a = ap.parse_args()
    except SystemExit:
        print("::error::THAM_SO_SAI")
        return 2
    for v in (a.base, a.head):
        if not re.fullmatch(r"[0-9a-f]{40}", v):
            print("::error::THAM_SO_SAI_SHA")
            return 2
    try:
        return run(a)
    except ToolError as e:
        print(f"::error::CONG_CU_LOI ({e})")
        return 2
    except Exception as e:  # không in thông điệp (có thể chứa tên file/dữ liệu)
        print(f"::error::CONG_CU_LOI ({type(e).__name__})")
        return 2


if __name__ == "__main__":
    sys.exit(main())
