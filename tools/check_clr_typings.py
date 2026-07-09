"""Validate the generated CLR stubs with pyright, end to end.

Two checks are run:
 1. Stub self-check  - pyright over the stub packages themselves (broken stubs,
	duplicate declarations, overlapping overloads).
 2. Example check    - pyright over every example in FLImagingExamplesPython with
	the stubs on the search path, measuring what users would actually see.

The stub packages are published as "FLImagingCLR-stubs" / "FLImagingClrPy-stubs"
(PEP 561 stub-only naming, resolved when installed into site-packages). pyright's
extraPaths does not apply that naming rule, so this script copies them into a work
directory without the "-stubs" suffix before checking.

Requires pyright (either "pyright" on PATH or npm/npx to fetch it).

Usage:
	python tools/check_clr_typings.py                    # regenerate stubs, then check
	python tools/check_clr_typings.py --typings <dir>    # check existing stub output
	python tools/check_clr_typings.py --max-rows 30      # more detail in summaries
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

SKIP_DIR_NAMES = {"tools", "typings", ".vs", ".git", "__pycache__"}

STUBS_PROJECT_CONFIG = """{
	"include": ["FLImagingCLR", "FLImagingClrPy"],
	"typeCheckingMode": "basic",
	"reportOverlappingOverload": "warning",
	"reportRedeclaration": "error",
	"reportSelfClsParameterName": true,
	"reportInvalidStubStatement": true,
	"pythonVersion": "3.10"
}
"""

EXAMPLES_PROJECT_CONFIG = """{
	"include": ["."],
	"extraPaths": ["../stubs", "Common"],
	"typeCheckingMode": "basic",
	"pythonVersion": "3.10"
}
"""


def FindPyrightCommand():
	for name in ("pyright", "pyright.cmd"):
		path = shutil.which(name)
		if path:
			return [path]

	for name in ("npx", "npx.cmd"):
		path = shutil.which(name)
		if path:
			return [path, "--yes", "pyright"]

	raise SystemExit("pyright not found: install it (npm install -g pyright) or make npx available on PATH.")


def RunPyright(command, project_dir):
	process = subprocess.run(
		command + ["--outputjson"],
		cwd=str(project_dir),
		capture_output=True,
		text=True,
		encoding="utf-8",
		errors="replace",
	)

	try:
		return json.loads(process.stdout)
	except json.JSONDecodeError:
		print(process.stdout)
		print(process.stderr, file=sys.stderr)
		raise SystemExit(f"pyright did not produce JSON output (exit code {process.returncode}).")


def GenerateStubs(work_dir, dll_dir):
	out_dir = work_dir / "typings-generated"
	command = [sys.executable, str(Path(__file__).resolve().parent / "generate_clr_typings.py"), "--out", str(out_dir)]
	if dll_dir is not None:
		command += ["--dll-dir", str(dll_dir)]

	print("Generating stubs...")
	process = subprocess.run(command)
	if process.returncode != 0:
		raise SystemExit("generate_clr_typings.py failed.")

	return out_dir


def PrepareStubsProject(work_dir, typings_dir):
	stubs_dir = work_dir / "stubs"
	stubs_dir.mkdir(parents=True)

	found = False
	for child in typings_dir.iterdir():
		if not child.is_dir():
			continue
		name = child.name[:-len("-stubs")] if child.name.endswith("-stubs") else child.name
		shutil.copytree(child, stubs_dir / name)
		found = True

	if not found:
		raise SystemExit(f"No stub packages found under {typings_dir}.")

	(stubs_dir / "pyrightconfig.json").write_text(STUBS_PROJECT_CONFIG, encoding="utf-8")
	return stubs_dir


def PrepareExamplesProject(work_dir, examples_dir):
	target_dir = work_dir / "examples"
	count = 0

	for path in examples_dir.rglob("*.py"):
		relative = path.relative_to(examples_dir)
		if any(part in SKIP_DIR_NAMES for part in relative.parts):
			continue
		destination = target_dir / relative
		destination.parent.mkdir(parents=True, exist_ok=True)
		shutil.copyfile(path, destination)
		count += 1

	if count == 0:
		raise SystemExit(f"No example .py files found under {examples_dir}.")

	(target_dir / "pyrightconfig.json").write_text(EXAMPLES_PROJECT_CONFIG, encoding="utf-8")
	return target_dir, count


def NormalizeMessage(message):
	first_line = message.splitlines()[0] if message else ""
	return re.sub(r'"[^"]*"', '"..."', first_line)


def Summarize(result, title, max_rows):
	summary = result.get("summary", {})
	diagnostics = result.get("generalDiagnostics", [])
	errors = [d for d in diagnostics if d.get("severity") == "error"]
	warnings = [d for d in diagnostics if d.get("severity") == "warning"]

	print()
	print(f"=== {title} ===")
	print(f"files analyzed: {summary.get('filesAnalyzed', '?')}   errors: {len(errors)}   warnings: {len(warnings)}   time: {summary.get('timeInSec', '?')}s")

	if not errors and not warnings:
		return

	rule_counts = Counter(d.get("rule", "<no rule>") for d in errors)
	if rule_counts:
		print("-- errors by rule --")
		for rule, count in rule_counts.most_common(max_rows):
			print(f"  {count:6d}  {rule}")

	message_counts = Counter(NormalizeMessage(d.get("message", "")) for d in errors)
	if message_counts:
		print("-- errors by message pattern --")
		for message, count in message_counts.most_common(max_rows):
			print(f"  {count:6d}  {message}")

	file_counts = Counter(Path(d.get("file", "?")).parent.name for d in errors)
	if file_counts:
		print("-- errors by directory --")
		for name, count in file_counts.most_common(max_rows):
			print(f"  {count:6d}  {name}")

	warning_counts = Counter((d.get("rule", "<no rule>"), NormalizeMessage(d.get("message", ""))) for d in warnings)
	if warning_counts:
		print("-- warnings --")
		for (rule, message), count in warning_counts.most_common(max_rows):
			print(f"  {count:6d}  [{rule}] {message}")


def main():
	repo_examples_dir = Path(__file__).resolve().parents[1]

	parser = argparse.ArgumentParser(description="Run pyright over the generated CLR stubs and the Python examples.")
	parser.add_argument("--typings", type=Path, default=None, help="Existing stub output directory (default: regenerate via generate_clr_typings.py).")
	parser.add_argument("--dll-dir", type=Path, default=None, help="Forwarded to generate_clr_typings.py when regenerating.")
	parser.add_argument("--examples", type=Path, default=repo_examples_dir, help="Examples root to type-check.")
	parser.add_argument("--work", type=Path, default=Path(tempfile.gettempdir()) / "flimaging-typing-check", help="Work directory (recreated on every run).")
	parser.add_argument("--max-rows", type=int, default=15, help="Rows per summary table.")
	parser.add_argument("--skip-examples", action="store_true", help="Only run the stub self-check.")
	args = parser.parse_args()

	pyright_command = FindPyrightCommand()

	if args.work.exists():
		shutil.rmtree(args.work)
	args.work.mkdir(parents=True)

	typings_dir = args.typings if args.typings is not None else GenerateStubs(args.work, args.dll_dir)
	if not typings_dir.exists():
		raise SystemExit(f"Typings directory not found: {typings_dir}")

	stubs_dir = PrepareStubsProject(args.work, typings_dir)
	stubs_result = RunPyright(pyright_command, stubs_dir)
	(args.work / "stubs_result.json").write_text(json.dumps(stubs_result, indent=1), encoding="utf-8")
	Summarize(stubs_result, "Stub self-check", args.max_rows)

	stub_errors = sum(1 for d in stubs_result.get("generalDiagnostics", []) if d.get("severity") == "error")

	if not args.skip_examples:
		examples_dir, example_count = PrepareExamplesProject(args.work, args.examples)
		print()
		print(f"Checking {example_count} example files...")
		examples_result = RunPyright(pyright_command, examples_dir)
		(args.work / "examples_result.json").write_text(json.dumps(examples_result, indent=1), encoding="utf-8")
		Summarize(examples_result, "Example check (user-visible surface)", args.max_rows)

	print()
	print(f"Raw pyright output kept in: {args.work}")
	return 1 if stub_errors else 0


if __name__ == "__main__":
	sys.exit(main())
