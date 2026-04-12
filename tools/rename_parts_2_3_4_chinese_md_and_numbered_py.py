"""
Rename Part 2–4 note .md files to NN-<Chinese title from first # heading>.md
and demo .py files to NN_<slug>_demo.py (or NN_<name>.py) aligned with note numbers.

Run from repo root:  python tools/rename_parts_2_3_4_chinese_md_and_numbered_py.py
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVALID_FS = '\\/:*?"<>|'

# Relative POSIX path -> fallback title when file has no H1
FALLBACK_MD_TITLE: dict[str, str] = {
    "part-4-control-flow/chapter-17/01-iterators-generators-classic-coroutines-intro.md": (
        "第17章开篇 迭代器与生成器及经典协程导引"
    ),
    "part-4-control-flow/chapter-17/12-generic-iterable-types.md": "17.12 泛型可迭代类型",
    "part-4-control-flow/chapter-17/13-classic-coroutines-type-hints.md": "17.13 经典协程与类型提示",
}

# (subdir under ROOT, old_py_name, new_py_name)
PY_RENAMES: list[tuple[str, str, str]] = []

# chapter-07
for old, new in [
    ("first_class_functions_demo.py", "01_first_class_functions_demo.py"),
    ("higher_order_functions_demo.py", "03_higher_order_functions_demo.py"),
    ("lambda_expressions_demo.py", "04_lambda_expressions_demo.py"),
    ("callable_objects_demo.py", "05_callable_objects_demo.py"),
    ("user_defined_callable_demo.py", "06_user_defined_callable_demo.py"),
    ("tag_and_positional_only_demo.py", "07_tag_and_positional_only_demo.py"),
    ("functional_tools_demo.py", "08_functional_tools_demo.py"),
]:
    PY_RENAMES.append(("part-2-functions-as-objects/chapter-07", old, new))

# chapter-08
for old, new in [
    ("type_hints_mypy_demo.py", "01_type_hints_mypy_demo.py"),
    ("gradual_typing_demo.py", "02_gradual_typing_demo.py"),
    ("show_count_demo.py", "03_show_count_demo.py"),
    ("duck_nominal_typing_demo.py", "04_duck_nominal_typing_demo.py"),
    ("types_in_annotations_demo.py", "05_types_in_annotations_demo.py"),
    ("types_advanced_demo.py", "06_types_advanced_demo.py"),
    ("tag_type_hints_demo.py", "07_tag_type_hints_demo.py"),
]:
    PY_RENAMES.append(("part-2-functions-as-objects/chapter-08", old, new))

# chapter-09
for old, new in [
    ("decorators_basics_demo.py", "02_decorators_basics_demo.py"),
    ("decorator_and_cache_demo.py", "02_decorator_and_cache_demo.py"),
    ("registration.py", "03_registration.py"),
    ("scope_dis_demo.py", "05_scope_dis_demo.py"),
    ("scope_closure_nonlocal_demo.py", "05_scope_closure_nonlocal_demo.py"),
    ("averager_closure_demo.py", "06_averager_closure_demo.py"),
    ("nonlocal_name_resolution_demo.py", "07_nonlocal_name_resolution_demo.py"),
    ("clock_decorator_demo.py", "08_clock_decorator_demo.py"),
    ("functools_decorators_demo.py", "09_functools_decorators_demo.py"),
    ("parameterized_decorators_demo.py", "10_parameterized_decorators_demo.py"),
]:
    PY_RENAMES.append(("part-2-functions-as-objects/chapter-09", old, new))

# chapter-10
for old, new in [
    ("strategy_promotions_demo.py", "02_strategy_promotions_demo.py"),
    ("strategy_auto_register_demo.py", "03_strategy_auto_register_demo.py"),
    ("command_pattern_demo.py", "04_command_pattern_demo.py"),
]:
    PY_RENAMES.append(("part-2-functions-as-objects/chapter-10", old, new))

# chapter-11
for old, new in [
    ("vector2d_repr_demo.py", "02_vector2d_repr_demo.py"),
    ("vector2d_frombytes_demo.py", "03_vector2d_frombytes_demo.py"),
    ("classmethod_staticmethod_demo.py", "04_classmethod_staticmethod_demo.py"),
    ("vector2d_format_demo.py", "05_vector2d_format_demo.py"),
    ("vector2d_hash_demo.py", "06_vector2d_hash_demo.py"),
    ("vector2d_match_demo.py", "07_vector2d_match_demo.py"),
    ("slots_inheritance_demo.py", "08_slots_inheritance_demo.py"),
    ("slots_memory_demo.py", "08_slots_memory_demo.py"),
    ("vector2d_typecode_override_demo.py", "09_vector2d_typecode_override_demo.py"),
    ("vector2d_v3.py", "09_vector2d_v3.py"),
]:
    PY_RENAMES.append(("part-3-classes-and-protocols/chapter-11", old, new))

# chapter-12
for old, new in [
    ("vector_len_getitem_demo.py", "02_vector_len_getitem_demo.py"),
    ("vector_v1_compat_demo.py", "03_vector_v1_compat_demo.py"),
    ("protocols_duck_typing_demo.py", "04_protocols_duck_typing_demo.py"),
    ("vector_v2_sequence_demo.py", "05_vector_v2_sequence_demo.py"),
    ("vector_v3_dynamic_attrs_demo.py", "06_vector_v3_dynamic_attrs_demo.py"),
    ("vector_v4_hash_eq_demo.py", "07_vector_v4_hash_eq_demo.py"),
    ("vector_v5_format_demo.py", "08_vector_v5_format_demo.py"),
]:
    PY_RENAMES.append(("part-3-classes-and-protocols/chapter-12", old, new))

# chapter-13
for old, new in [
    ("typesystems_duck_goose_protocol_demo.py", "01_typesystems_duck_goose_protocol_demo.py"),
    ("dynamic_static_protocols_demo.py", "03_dynamic_static_protocols_demo.py"),
    ("duck_typing_practice_demo.py", "04_duck_typing_practice_demo.py"),
    ("goose_typing_abcs_demo.py", "05_goose_typing_abcs_demo.py"),
    ("virtual_subclass_and_subclasshook_demo.py", "06_virtual_subclass_and_subclasshook_demo.py"),
    ("static_protocols_demo.py", "07_static_protocols_demo.py"),
]:
    PY_RENAMES.append(("part-3-classes-and-protocols/chapter-13", old, new))

# chapter-14
for old, new in [
    ("super_last_updated_ordereddict_demo.py", "02_super_last_updated_ordereddict_demo.py"),
    ("super_mro_diamond_demo.py", "02_super_mro_diamond_demo.py"),
    ("builtin_subclass_pitfalls_demo.py", "03_builtin_subclass_pitfalls_demo.py"),
    ("mro_diamond_root_ab_leaf_demo.py", "04_mro_diamond_root_ab_leaf_demo.py"),
    ("real_world_mixins_demo.py", "06_real_world_mixins_demo.py"),
]:
    PY_RENAMES.append(("part-3-classes-and-protocols/chapter-14", old, new))

# chapter-15
for old, new in [
    ("overload_demo.py", "02_overload_demo.py"),
    ("max_like_overload_demo.py", "02_max_like_overload_demo.py"),
    ("typeddict_demo.py", "03_typeddict_demo.py"),
    ("cast_demo.py", "04_cast_demo.py"),
    ("type_narrowing_demo.py", "04_type_narrowing_demo.py"),
    ("runtime_type_hints_demo.py", "05_runtime_type_hints_demo.py"),
    ("reading_type_hints_demo.py", "05_reading_type_hints_demo.py"),
    ("generic_class_lotto_demo.py", "06_generic_class_lotto_demo.py"),
    ("generics_variance_demo.py", "07_generics_variance_demo.py"),
    ("variance_vending_trash_demo.py", "07_variance_vending_trash_demo.py"),
    ("generic_protocol_demo.py", "08_generic_protocol_demo.py"),
    ("generic_static_protocol_demo.py", "08_generic_static_protocol_demo.py"),
]:
    PY_RENAMES.append(("part-3-classes-and-protocols/chapter-15", old, new))

# chapter-16
for old, new in [
    ("operator_overloading_intro_demo.py", "01_operator_overloading_intro_demo.py"),
    ("unary_operators_demo.py", "03_unary_operators_demo.py"),
    ("vector_add_operator_demo.py", "04_vector_add_operator_demo.py"),
    ("addable_bingo_cage_demo.py", "07_addable_bingo_cage_demo.py"),
]:
    PY_RENAMES.append(("part-3-classes-and-protocols/chapter-16", old, new))

# part-4 chapter-17
for old, new in [
    ("sentence_sequence_protocol_demo.py", "02_sentence_sequence_protocol_demo.py"),
    ("iter_builtin_demo.py", "03_iter_builtin_demo.py"),
    ("iterables_vs_iterators_demo.py", "04_iterables_vs_iterators_demo.py"),
    ("sentence_iterator_generator_demo.py", "05_sentence_iterator_generator_demo.py"),
    ("lazy_sentence_demo.py", "06_lazy_sentence_demo.py"),
    ("generator_expressions_demo.py", "07_generator_expressions_demo.py"),
    ("arithmetic_progression_demo.py", "08_arithmetic_progression_demo.py"),
    ("itertools_toolbox_demo.py", "09_itertools_toolbox_demo.py"),
    ("reduction_and_yield_from_demo.py", "10_reduction_and_yield_from_demo.py"),
]:
    PY_RENAMES.append(("part-4-control-flow/chapter-17", old, new))

# chapter-18
for old, new in [
    ("looking_glass_context_manager_demo.py", "02_looking_glass_context_manager_demo.py"),
    ("lispy_match_case_demo.py", "03_lispy_match_case_demo.py"),
    ("else_clauses_demo.py", "04_else_clauses_demo.py"),
]:
    PY_RENAMES.append(("part-4-control-flow/chapter-18", old, new))

# chapter-19
for old, new in [
    ("concurrency_vs_parallelism_demo.py", "00_concurrency_vs_parallelism_demo.py"),
    ("gil_and_execution_units_demo.py", "01_gil_and_execution_units_demo.py"),
    ("spinner_concurrency_demo.py", "04_spinner_concurrency_demo.py"),
    ("prime_spinner_gil_demo.py", "05_prime_spinner_gil_demo.py"),
    ("manual_process_pool_primes_demo.py", "06_manual_process_pool_primes_demo.py"),
]:
    PY_RENAMES.append(("part-4-control-flow/chapter-19", old, new))

# chapter-20
for old, new in [
    ("executors_and_futures_demo.py", "00_executors_and_futures_demo.py"),
    ("flags_threadpool_download_demo.py", "02_flags_threadpool_download_demo.py"),
    ("process_pool_primes_demo.py", "03_process_pool_primes_demo.py"),
    ("executor_map_scheduling_demo.py", "04_executor_map_scheduling_demo.py"),
    ("flags2_threadpool_progress_demo.py", "05_flags2_threadpool_progress_demo.py"),
]:
    PY_RENAMES.append(("part-4-control-flow/chapter-20", old, new))

# chapter-21
for old, new in [
    ("async_blocking_pitfall_demo.py", "00_async_blocking_pitfall_demo.py"),
    ("coroutine_types_demo.py", "02_coroutine_types_demo.py"),
    ("blogdom_probe_demo.py", "03_blogdom_probe_demo.py"),
    ("flags_asyncio_httpx_demo.py", "04_flags_asyncio_httpx_demo.py"),
    ("flags2_asyncio_progress_demo.py", "05_flags2_asyncio_progress_demo.py"),
    ("offload_to_thread_and_process_demo.py", "06_offload_to_thread_and_process_demo.py"),
    ("tcp_mojifinder_demo.py", "06_tcp_mojifinder_demo.py"),
    ("tcp_mojifinder_client_demo.py", "06_tcp_mojifinder_client_demo.py"),
    ("web_mojifinder_fastapi_demo.py", "06_web_mojifinder_fastapi_demo.py"),
    ("async_iteration_demo.py", "10_async_iteration_demo.py"),
    ("curio_taskgroup_probe_demo.py", "11_curio_taskgroup_probe_demo.py"),
]:
    PY_RENAMES.append(("part-4-control-flow/chapter-21", old, new))


def sanitize_title(s: str) -> str:
    s = s.replace("`", "")
    for c in INVALID_FS:
        s = s.replace(c, " ")
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) > 100:
        s = s[:100].rstrip()
    return s


def first_h1(text: str) -> str | None:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def collect_md_renames() -> list[tuple[Path, Path]]:
    pairs: list[tuple[Path, Path]] = []
    dest_names: dict[Path, set[str]] = {}
    for part in [
        ROOT / "part-2-functions-as-objects",
        ROOT / "part-3-classes-and-protocols",
        ROOT / "part-4-control-flow",
    ]:
        for md in sorted(part.rglob("*.md")):
            if md.name.lower() == "readme.md":
                continue
            rel_posix = md.relative_to(ROOT).as_posix()
            text = md.read_text(encoding="utf-8")
            title = first_h1(text)
            if not title:
                title = FALLBACK_MD_TITLE.get(rel_posix)
            if not title:
                print(f"SKIP md (no title): {rel_posix}", file=sys.stderr)
                continue
            m = re.match(r"^(\d{2})-", md.name)
            num = m.group(1) if m else None
            if not num and md.stem == "inheritance-cheatsheet":
                num = "05"
            if not num:
                print(f"SKIP md (no NN prefix): {rel_posix}", file=sys.stderr)
                continue
            new_name = f"{num}-{sanitize_title(title)}.md"
            if new_name == md.name:
                continue
            parent = md.parent
            taken = dest_names.setdefault(parent, set())
            base_title = sanitize_title(title)
            suffix_n = 2
            while new_name in taken:
                new_name = f"{num}-{base_title}-{suffix_n}.md"
                suffix_n += 1
            taken.add(new_name)
            dest = md.with_name(new_name)
            pairs.append((md, dest))
    return pairs


def git_mv(src: Path, dst: Path) -> None:
    subprocess.run(["git", "mv", str(src), str(dst)], cwd=ROOT, check=True)


def main() -> None:
    md_pairs = collect_md_renames()

    # --- MD renames (two-phase if swap/collision; here linear git mv) ---
    for src, dst in md_pairs:
        if dst.exists() and dst != src:
            raise SystemExit(f"Target exists: {dst}")
    for src, dst in md_pairs:
        if src != dst:
            print(f"git mv md: {src.name} -> {dst.name}")
            git_mv(src, dst)
    for src, dst in md_pairs:
        rel_old = src.relative_to(ROOT).as_posix()
        if rel_old in FALLBACK_MD_TITLE and dst.exists():
            body = dst.read_text(encoding="utf-8").strip()
            if len(body) < 4:
                line = "# " + FALLBACK_MD_TITLE[rel_old] + "\n\n"
                dst.write_text(line, encoding="utf-8", newline="\n")
                print(f"fill stub: {dst.relative_to(ROOT)}")

    # --- PY renames ---
    for sub, old, new in PY_RENAMES:
        src = ROOT / sub / old
        dst = ROOT / sub / new
        if not src.exists():
            raise SystemExit(f"Missing py: {src}")
        if src == dst:
            continue
        if dst.exists():
            raise SystemExit(f"Target exists: {dst}")
        print(f"git mv py: {sub}/{old} -> {new}")
        git_mv(src, dst)

    # --- Text substitution (basenames) ---
    subs: list[tuple[str, str]] = []
    for a, b in md_pairs:
        subs.append((a.name, b.name))
    for sub, old, new in PY_RENAMES:
        subs.append((old, new))
    subs.sort(key=lambda x: len(x[0]), reverse=True)

    skip_parts = (".git", "__pycache__")
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        if any(p in path.parts for p in skip_parts):
            continue
        if path.suffix.lower() not in (".md", ".py", ".txt"):
            continue
        if path.resolve() == Path(__file__).resolve():
            continue
        text = path.read_text(encoding="utf-8")
        orig = text
        for o, n in subs:
            if o == n:
                continue
            text = text.replace(o, n)
        if text != orig:
            path.write_text(text, encoding="utf-8", newline="\n")
            print(f"patched: {path.relative_to(ROOT)}")

    # chapter-11: fix dynamic loads to new repr / v3 basenames
    ch11 = ROOT / "part-3-classes-and-protocols/chapter-11"
    for py in ch11.glob("*.py"):
        t = py.read_text(encoding="utf-8")
        t2 = t.replace('"vector2d_repr_demo.py"', '"02_vector2d_repr_demo.py"')
        t2 = t2.replace('"vector2d_v3.py"', '"09_vector2d_v3.py"')
        if t2 != t:
            py.write_text(t2, encoding="utf-8", newline="\n")
            print(f"patched loads: {py.name}")

    print("Done.")


if __name__ == "__main__":
    main()
