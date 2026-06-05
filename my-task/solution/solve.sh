#!/usr/bin/env bash
set -euo pipefail

git apply --whitespace=fix << 'PATCH'
diff --git a/hysteresis.py b/hysteresis.py
--- a/hysteresis.py
+++ b/hysteresis.py
@@ -38,7 +38,7 @@ class HysteresisManager:
                 self.consecutive_count += 1
                 if self.consecutive_count >= self.required_consecutive:
                     self.current_status = "OK"
-                    # consecutive_count not reset — persists into next state evaluation
+                    self.consecutive_count = 0
             else:
                 self.consecutive_count = 0
PATCH
