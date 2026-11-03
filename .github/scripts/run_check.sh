#!/usr/bin/env bash
# run_check.sh — chạy từ bản TIN CẬY (trusted/ = main). Nội dung PR chỉ là DỮ LIỆU.
# Không checkout, không chạy, không cài, không source file nào của PR.
# Vào (env): PR_NUMBER, HEAD_SHA, BASE_SHA, REPO_URL.  Không secret.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Cô lập git: không config hệ thống/người dùng, không hook, không hỏi mật khẩu.
export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_TERMINAL_PROMPT=0
export GIT_LFS_SKIP_SMUDGE=1
G=(git -c core.hooksPath=/dev/null -c protocol.allow=never -c protocol.https.allow=always -c protocol.file.allow=never)

fail () { echo "::error::$1"; exit 1; }
[[ "${PR_NUMBER:-}" =~ ^[0-9]{1,9}$ ]]   || fail "THAM_SO_SAI_PR_NUMBER"
[[ "${HEAD_SHA:-}"  =~ ^[0-9a-f]{40}$ ]] || fail "THAM_SO_SAI_HEAD_SHA"
[[ "${BASE_SHA:-}"  =~ ^[0-9a-f]{40}$ ]] || fail "THAM_SO_SAI_BASE_SHA"
[[ -n "${REPO_URL:-}" ]]                 || fail "THAM_SO_SAI_REPO_URL"

PRDIR="${RUNNER_TEMP:-$(mktemp -d)}/pr"
rm -rf "$PRDIR"
"${G[@]}" init -q --bare "$PRDIR" >/dev/null 2>&1 || fail "GIT_INIT_LOI"
# Chỉ tải đối tượng git (bare repo, không worktree => không smudge/filter/LFS/submodule).
# refs/pull/N/head có thể cập nhật chậm hơn sự kiện -> thử tối đa 3 lần, cách 5 giây.
for TRY in 1 2 3; do
  "${G[@]}" -C "$PRDIR" fetch -q --no-tags --no-recurse-submodules --no-write-fetch-head "$REPO_URL" \
    "+refs/heads/main:refs/pr/main" "+refs/pull/${PR_NUMBER}/head:refs/pr/head" >/dev/null 2>&1 \
    || fail "GIT_FETCH_LOI"
  GOT="$("${G[@]}" -C "$PRDIR" rev-parse refs/pr/head 2>/dev/null)" || fail "HEAD_KHONG_CO"
  [[ "$GOT" == "$HEAD_SHA" ]] && break
  # Vẫn khác sau 3 lần (PR được push thêm) -> không kiểm bản khác; sự kiện mới sẽ chạy lại.
  [[ "$TRY" -lt 3 ]] || fail "HEAD_DA_DOI (đợi lần chạy mới)"
  echo "::notice::HEAD_CHUA_KHOP_THU_LAI ($TRY/3)"
  sleep 5
done
"${G[@]}" -C "$PRDIR" cat-file -e "${BASE_SHA}^{commit}" >/dev/null 2>&1 || fail "BASE_KHONG_CO"

exec python3 -I "$HERE/pr_check.py" --repo "$PRDIR" --base "$BASE_SHA" --head "$HEAD_SHA"
