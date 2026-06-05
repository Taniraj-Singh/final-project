#!/usr/bin/env bash
set -euo pipefail

git apply --whitespace=fix << 'PATCH'
--- a/hysteresis.py
+++ b/hysteresis.py
@@ -36,7 +36,7 @@ class HysteresisManager:
         else:  # anomaly_score < warn_threshold
             if self.current_status != "OK":
                 self.consecutive_count += 1
                 if self.consecutive_count >= self.required_consecutive:
                     self.current_status = "OK"
-                    # consecutive_count not reset — persists into next state evaluation
+                    self.consecutive_count = 0
             else:
                 self.consecutive_count = 0
PATCH
