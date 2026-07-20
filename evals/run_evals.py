#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
scripts = ROOT/"scripts"
results = []
# good pack validate
r = subprocess.run([sys.executable, str(scripts/"handoff_pack.py"), "validate", "--root", str(ROOT/"evals/fixtures/good_pack"), "--json"], capture_output=True, text=True)
good = json.loads(r.stdout)
results.append({"case":"good_pack_validate", "decision": good["decision"], "expect":"PASS", "pass": good["decision"]=="PASS"})
r = subprocess.run([sys.executable, str(scripts/"handoff_pack.py"), "validate", "--root", str(ROOT/"evals/fixtures/bad_pack"), "--json"], capture_output=True, text=True)
bad = json.loads(r.stdout)
results.append({"case":"bad_pack_validate", "decision": bad["decision"], "expect":"FAIL", "pass": bad["decision"]=="FAIL"})
r = subprocess.run([sys.executable, str(scripts/"verify_gate.py"), "--root", str(ROOT/"evals/fixtures/good_pack"), "--min-chapter-words", "800", "--json"], capture_output=True, text=True)
vg = json.loads(r.stdout)
results.append({"case":"good_verify_gate", "decision": vg["decision"], "expect":"PASS", "pass": vg["decision"]=="PASS"})
r = subprocess.run([sys.executable, str(scripts/"verify_gate.py"), "--root", str(ROOT/"evals/fixtures/bad_pack"), "--min-chapter-words", "800", "--json"], capture_output=True, text=True)
vb = json.loads(r.stdout)
results.append({"case":"bad_verify_gate", "decision": vb["decision"], "expect":"FAIL", "pass": vb["decision"]=="FAIL"})
r = subprocess.run([sys.executable, str(scripts/"assist_mode_router.py"), "--text", "write a Storybook story for Button", "--json"], capture_output=True, text=True)
ab = json.loads(r.stdout)
results.append({"case":"abstain_storybook", "decision": ab["decision"], "expect":"ABSTAIN", "pass": ab["decision"]=="ABSTAIN"})
r = subprocess.run([sys.executable, str(scripts/"ai_tells_ensemble.py"), "--root", str(ROOT/"evals/fixtures/ai_tells_pack")], capture_output=True, text=True)
ait = json.loads(r.stdout)
results.append({"case":"ai_tells_planted_fail", "decision": ait["decision"], "expect":"FAIL", "pass": ait["decision"]=="FAIL"})
r = subprocess.run([sys.executable, str(scripts/"ai_tells_ensemble.py"), "--root", str(ROOT/"evals/fixtures/good_pack")], capture_output=True, text=True)
aitg = json.loads(r.stdout)
results.append({"case":"ai_tells_good_pass", "decision": aitg["decision"], "expect":"PASS", "pass": aitg["decision"]=="PASS"})
# compose should not prescribe the entire marketplace
r = subprocess.run([sys.executable, str(scripts/"compose.py"), "--root", str(ROOT/"evals/fixtures/ai_tells_pack"), "--write"], capture_output=True, text=True)
comp = json.loads(r.stdout)
n_members = len((comp.get("prescription") or {}).get("members") or [])
has_pair = bool((comp.get("prescription") or {}).get("detector_scrubber_pairs"))
results.append({"case":"compose_minimal", "n_members": n_members, "expect":"<=5", "pass": n_members <= 5 and n_members >= 1})
results.append({"case":"compose_adversarial_pair", "has_pair": has_pair, "expect": True, "pass": has_pair is True})
# good pack verify should pass under compound gate
r = subprocess.run([sys.executable, str(scripts/"verify_gate.py"), "--root", str(ROOT/"evals/fixtures/good_pack"), "--json"], capture_output=True, text=True)
vg2 = json.loads(r.stdout)
results.append({"case":"good_verify_compound", "decision": vg2["decision"], "compound": vg2.get("compound_pressure"), "expect":"PASS", "pass": vg2["decision"]=="PASS"})
ok = all(x["pass"] for x in results)
print(json.dumps({"decision":"PASS" if ok else "FAIL", "results": results}, indent=2))
raise SystemExit(0 if ok else 1)
