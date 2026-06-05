Set-Location "c:\Users\Taniraj\final-project"

function Commit($msg) {
    git add -A
    git commit -m $msg
}

# ── Commit 3: add pytest infrastructure and clean Dockerfile ──────────────────
Commit "Add pytest unit tests and Silver-compliant Dockerfile"

# ── Commit 4: introduce Bug A — RingBuffer.clear() does not reset is_full ─────
$bufContent = Get-Content "buffer.py" -Raw
$buggyBuf = $bufContent -replace "        self\.buffer = \[\]\r?\n        self\.is_full = False", "        self.buffer = []"
Set-Content "buffer.py" $buggyBuf -NoNewline
Commit "Refactor RingBuffer.clear() to simplify reset logic"

# ── Commit 5: fix Bug A ───────────────────────────────────────────────────────
Set-Content "buffer.py" $bufContent -NoNewline
Commit "Fix RingBuffer.clear() to properly reset is_full flag"

# ── Commit 6: introduce Bug B — RingBuffer.is_ready() wrong threshold ─────────
$bufContent2 = Get-Content "buffer.py" -Raw
$buggyBuf2 = $bufContent2 -replace "return len\(self\.buffer\) >= self\.window_size", "return len(self.buffer) > self.window_size"
Set-Content "buffer.py" $buggyBuf2 -NoNewline
Commit "Optimize RingBuffer readiness check to use strict inequality"

# ── Commit 7: fix Bug B ───────────────────────────────────────────────────────
Set-Content "buffer.py" $bufContent2 -NoNewline
Commit "Fix RingBuffer.is_ready() off-by-one: use >= not >"

# ── Commit 8: introduce Bug C — HysteresisManager consecutive_count not reset on OK path ──
$hystContent = Get-Content "hysteresis.py" -Raw
$buggyHyst = $hystContent -replace "        else:  # anomaly_score < warn_threshold\r?\n            if self\.current_status != ""OK"":\r?\n                self\.consecutive_count \+= 1\r?\n                if self\.consecutive_count >= self\.required_consecutive:\r?\n                    self\.current_status = ""OK""\r?\n                    self\.consecutive_count = 0\r?\n            else:\r?\n                self\.consecutive_count = 0", "        else:  # anomaly_score < warn_threshold`n            if self.current_status != `"OK`":`n                self.consecutive_count += 1`n                if self.consecutive_count >= self.required_consecutive:`n                    self.current_status = `"OK`""
Set-Content "hysteresis.py" $buggyHyst -NoNewline
Commit "Streamline OK recovery path in HysteresisManager"

# ── Commit 9: fix Bug C ───────────────────────────────────────────────────────
Set-Content "hysteresis.py" $hystContent -NoNewline
Commit "Fix HysteresisManager: reset consecutive_count after OK transition"
