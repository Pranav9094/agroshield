# -*- coding: utf-8 -*-
"""
AgroShield Integration Test Suite
==================================
Tests the complete AgroShield pipeline end-to-end.

Usage:
    python integration_test.py
    python integration_test.py --image path/to/farm.jpg
    python integration_test.py --backend http://localhost:8000 --frontend http://localhost:5173
"""

import sys
import time
import json
import argparse
import requests
import io
from pathlib import Path

# Force UTF-8 output on Windows so box/emoji chars don't crash cp1252
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# ── Colorama setup ────────────────────────────────────────────────────────────
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    print("[WARNING] colorama not installed. Run: pip install colorama")
    # Graceful fallback — no colors
    class Fore:
        GREEN = RED = YELLOW = CYAN = MAGENTA = WHITE = BLUE = ""
    class Style:
        BRIGHT = RESET_ALL = DIM = ""

# ── Constants ─────────────────────────────────────────────────────────────────
PERFORMANCE_THRESHOLD_SEC = 3.0

DETECT_REQUIRED_FIELDS = {
    "weed_count": int,
    "detections": list,
    "spray_points": list,
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def _tag(passed: bool) -> str:
    if passed:
        return f"{Fore.GREEN}{Style.BRIGHT}  PASS  {Style.RESET_ALL}"
    return f"{Fore.RED}{Style.BRIGHT}  FAIL  {Style.RESET_ALL}"


def _section(title: str):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'-' * 55}")
    print(f"  {title}")
    print(f"{'-' * 55}{Style.RESET_ALL}")


def _info(label: str, value):
    print(f"  {Style.DIM}{label:<20}{Style.RESET_ALL}{value}")


def _elapsed(seconds: float) -> str:
    colour = Fore.GREEN if seconds < PERFORMANCE_THRESHOLD_SEC else Fore.RED
    label  = "FAST" if seconds < PERFORMANCE_THRESHOLD_SEC else "SLOW"
    return f"{colour}{Style.BRIGHT}{label}{Style.RESET_ALL} ({seconds:.3f}s)"


# ── Individual tests ──────────────────────────────────────────────────────────

def test_backend_health(backend_url: str) -> tuple[bool, str]:
    """Test 1 — Backend health check: GET /health → {'status': 'ok'}"""
    url = f"{backend_url}/health"
    try:
        resp = requests.get(url, timeout=10)
        body = resp.json()
        passed = resp.status_code == 200 and body.get("status") == "ok"
        detail = f"HTTP {resp.status_code} | body={body}"
        return passed, detail
    except requests.exceptions.ConnectionError:
        return False, f"Connection refused — is the backend running at {backend_url}?"
    except Exception as exc:
        return False, str(exc)


def test_frontend_reachability(frontend_url: str) -> tuple[bool, str]:
    """Test 2 — Frontend reachability: GET root → 200"""
    try:
        resp = requests.get(frontend_url, timeout=10)
        passed = resp.status_code == 200
        detail = f"HTTP {resp.status_code}"
        return passed, detail
    except requests.exceptions.ConnectionError:
        return False, f"Connection refused — is the frontend running at {frontend_url}?"
    except Exception as exc:
        return False, str(exc)


def test_detection(backend_url: str, image_path: Path) -> tuple[bool, str, dict | None, float]:
    """Test 3 — POST /detect with image → weed_count, detections, spray_points"""
    url = f"{backend_url}/detect"
    if not image_path.exists():
        return False, f"Image not found: {image_path}", None, 0.0

    try:
        with open(image_path, "rb") as f:
            files = {"file": (image_path.name, f, "image/jpeg")}
            t0 = time.perf_counter()
            resp = requests.post(url, files=files, timeout=30)
            elapsed = time.perf_counter() - t0

        if resp.status_code != 200:
            return False, f"HTTP {resp.status_code}: {resp.text[:200]}", None, elapsed

        body = resp.json()
        return True, f"HTTP {resp.status_code}", body, elapsed

    except requests.exceptions.ConnectionError:
        return False, f"Connection refused — is the backend running at {backend_url}?", None, 0.0
    except Exception as exc:
        return False, str(exc), None, 0.0


def test_schema_validation(response_body: dict | None) -> tuple[bool, str]:
    """Test 4 — Validate required fields + types in /detect response"""
    if response_body is None:
        return False, "No response body to validate (detection test failed)"

    missing = []
    wrong_type = []

    for field, expected_type in DETECT_REQUIRED_FIELDS.items():
        if field not in response_body:
            missing.append(field)
        elif not isinstance(response_body[field], expected_type):
            actual = type(response_body[field]).__name__
            wrong_type.append(f"{field} (expected {expected_type.__name__}, got {actual})")

    if missing or wrong_type:
        issues = []
        if missing:
            issues.append(f"Missing fields: {missing}")
        if wrong_type:
            issues.append(f"Wrong types: {wrong_type}")
        return False, " | ".join(issues)

    # Extra: validate detections list items have expected sub-keys
    detections: list = response_body["detections"]
    if detections:
        expected_detection_keys = {"bbox", "confidence", "class"}
        first = detections[0]
        missing_sub = expected_detection_keys - set(first.keys())
        if missing_sub:
            return False, f"Detection item missing keys: {missing_sub}"

    return True, (
        f"weed_count={response_body['weed_count']} | "
        f"detections={len(response_body['detections'])} | "
        f"spray_points={len(response_body['spray_points'])}"
    )


def test_performance(elapsed: float) -> tuple[bool, str]:
    """Test 5 — Response time < 3s"""
    passed = elapsed < PERFORMANCE_THRESHOLD_SEC
    label  = "FAST" if passed else "SLOW"
    return passed, f"{label} — {elapsed:.3f}s (threshold: {PERFORMANCE_THRESHOLD_SEC}s)"


# ── Runner ────────────────────────────────────────────────────────────────────

def run_all(backend_url: str, frontend_url: str, image_path: Path):
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}")
    print("  +==================================================+")
    print("  |       AgroShield Integration Test Suite          |")
    print("  +==================================================+")
    print(Style.RESET_ALL)
    print(f"  Backend  : {Fore.YELLOW}{backend_url}{Style.RESET_ALL}")
    print(f"  Frontend : {Fore.YELLOW}{frontend_url}{Style.RESET_ALL}")
    print(f"  Image    : {Fore.YELLOW}{image_path}{Style.RESET_ALL}")

    results: list[tuple[str, bool, str]] = []  # (name, passed, detail)

    # ── Test 1 ────────────────────────────────────────────────────────────────
    _section("Test 1 — Backend Health Check")
    t1_ok, t1_detail = test_backend_health(backend_url)
    print(f"  {_tag(t1_ok)}  GET {backend_url}/health")
    _info("Result:", t1_detail)
    results.append(("Backend Health Check", t1_ok, t1_detail))

    # ── Test 2 ────────────────────────────────────────────────────────────────
    _section("Test 2 — Frontend Reachability")
    t2_ok, t2_detail = test_frontend_reachability(frontend_url)
    print(f"  {_tag(t2_ok)}  GET {frontend_url}")
    _info("Result:", t2_detail)
    results.append(("Frontend Reachability", t2_ok, t2_detail))

    # ── Test 3 ────────────────────────────────────────────────────────────────
    _section("Test 3 — Weed Detection (POST /detect)")
    t3_ok, t3_detail, response_body, elapsed = test_detection(backend_url, image_path)
    print(f"  {_tag(t3_ok)}  POST {backend_url}/detect  [{image_path.name}]")
    _info("Result:", t3_detail)
    if response_body:
        _info("Response:", json.dumps(response_body, indent=2)[:400])
    results.append(("Detection Test", t3_ok, t3_detail))

    # ── Test 4 ────────────────────────────────────────────────────────────────
    _section("Test 4 — JSON Schema Validation")
    t4_ok, t4_detail = test_schema_validation(response_body)
    print(f"  {_tag(t4_ok)}  Required fields: weed_count, detections, spray_points")
    _info("Result:", t4_detail)
    results.append(("Schema Validation", t4_ok, t4_detail))

    # ── Test 5 ────────────────────────────────────────────────────────────────
    _section("Test 5 — Performance (<3s threshold)")
    t5_ok, t5_detail = test_performance(elapsed)
    print(f"  {_tag(t5_ok)}  Detection response time → {_elapsed(elapsed)}")
    _info("Result:", t5_detail)
    results.append(("Performance Test", t5_ok, t5_detail))

    # ── Summary ───────────────────────────────────────────────────────────────
    passing = sum(1 for _, ok, _ in results if ok)
    total   = len(results)
    failing = [(name, detail) for name, ok, detail in results if not ok]

    score_colour = Fore.GREEN if passing == total else (Fore.YELLOW if passing >= 3 else Fore.RED)

    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 55}")
    print(f"  FINAL SCORE: {score_colour}{Style.BRIGHT}{passing}/{total}{Fore.CYAN}  tests passed")
    print(f"{'=' * 55}{Style.RESET_ALL}\n")

    if failing:
        print(f"{Fore.RED}{Style.BRIGHT}  [X] Failing tests:{Style.RESET_ALL}")
        for name, detail in failing:
            print(f"    {Fore.RED}  - {name}{Style.RESET_ALL}")
            print(f"      {Style.DIM}{detail}{Style.RESET_ALL}")
        print()
    else:
        print(f"  {Fore.GREEN}{Style.BRIGHT}[OK] All tests passed! AgroShield pipeline is healthy.{Style.RESET_ALL}\n")

    return passing, total


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AgroShield Integration Test Suite")
    parser.add_argument(
        "--backend",
        default="http://localhost:8000",
        help="Backend base URL (default: http://localhost:8000)",
    )
    parser.add_argument(
        "--frontend",
        default="http://localhost:5173",
        help="Frontend base URL (default: http://localhost:5173)",
    )
    parser.add_argument(
        "--image",
        default="sample_farm.jpg",
        help="Path to sample farm image for detection test (default: sample_farm.jpg)",
    )
    args = parser.parse_args()

    passing, total = run_all(
        backend_url=args.backend,
        frontend_url=args.frontend,
        image_path=Path(args.image),
    )

    # Exit code: 0 if all pass, 1 if any fail
    sys.exit(0 if passing == total else 1)
