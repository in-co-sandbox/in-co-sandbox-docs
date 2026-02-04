#!/usr/bin/env python3
"""
Review a single OpenAPI operation for "spec-as-documentation" quality.

This script is intentionally lightweight:
- Standard library only (JSON only; no YAML dependency).
- Focuses on common doc-quality gaps (missing summaries, descriptions, examples, schema docs).

Usage (from repo root):
  python -X utf8 ai/skills/openapi-spec-reviewer/scripts/review_openapi_operation.py --mdx <endpoint.mdx>
  python -X utf8 ai/skills/openapi-spec-reviewer/scripts/review_openapi_operation.py --spec <openapi.json> --method POST --path /route
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


HTTP_METHODS = {"get", "put", "post", "delete", "patch", "head", "options", "trace"}


@dataclass(frozen=True)
class OperationRef:
    spec_path: Path
    method: str
    route_path: str
    source: str


@dataclass(frozen=True)
class Issue:
    severity: str
    pointer: str
    message: str
    suggestion: str | None = None


def json_pointer_escape(token: str) -> str:
    return token.replace("~", "~0").replace("/", "~1")


def join_pointer(*tokens: str) -> str:
    return "#/" + "/".join(json_pointer_escape(token) for token in tokens)


def find_repo_root(start: Path) -> Path:
    start = start.resolve()
    for candidate in [start, *start.parents]:
        if (candidate / "docs.json").is_file() and (candidate / "api-reference").is_dir():
            return candidate
    return Path.cwd().resolve()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def parse_mdx_openapi_value(mdx_path: Path) -> str:
    text = read_text(mdx_path)
    match = re.match(r"^---\s*\r?\n(.*?)\r?\n---\s*(?:\r?\n|$)", text, flags=re.DOTALL)
    if not match:
        raise ValueError(f"Missing YAML frontmatter in {mdx_path}")

    frontmatter = match.group(1).splitlines()
    for line in frontmatter:
        stripped = line.strip()
        if not stripped.startswith("openapi:"):
            continue
        value = stripped.split(":", 1)[1].strip()
        if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
            value = value[1:-1]
        return value.strip()

    raise ValueError(f"Missing 'openapi:' field in frontmatter of {mdx_path}")


def parse_openapi_ref(openapi_value: str) -> tuple[str, str, str]:
    # Expected: "<specPath> <METHOD> <PATH>"
    parts = openapi_value.strip().split()
    if len(parts) < 3:
        raise ValueError(f"Invalid openapi reference: {openapi_value!r}")
    spec = parts[0].strip()
    method = parts[1].strip().upper()
    route_path = " ".join(parts[2:]).strip()
    if not route_path.startswith("/"):
        route_path = "/" + route_path
    return spec, method, route_path


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc


def get_operation(spec: dict[str, Any], method: str, route_path: str) -> tuple[dict[str, Any], str, str]:
    paths = spec.get("paths")
    if not isinstance(paths, dict):
        raise ValueError("Spec is missing top-level 'paths' object")

    path_item = paths.get(route_path)
    if not isinstance(path_item, dict):
        candidates = difflib.get_close_matches(route_path, list(paths.keys()), n=5)
        hint = f" Closest paths: {', '.join(candidates)}" if candidates else ""
        raise KeyError(f"Path not found in spec: {route_path}.{hint}")

    op = path_item.get(method.lower())
    if not isinstance(op, dict):
        available = [k.upper() for k in path_item.keys() if k in HTTP_METHODS]
        hint = f" Available methods for this path: {', '.join(sorted(available))}" if available else ""
        raise KeyError(f"Operation not found: {method} {route_path}.{hint}")

    return op, route_path, method.lower()


def iter_schema_refs(schema: Any) -> Iterable[str]:
    if not isinstance(schema, dict):
        return

    ref = schema.get("$ref")
    if isinstance(ref, str):
        yield ref

    for key, value in schema.items():
        if key in {"$ref", "example"}:
            continue
        if isinstance(value, dict):
            yield from iter_schema_refs(value)
        elif isinstance(value, list):
            for item in value:
                yield from iter_schema_refs(item)


def resolve_ref(spec: dict[str, Any], ref: str) -> Any | None:
    if not ref.startswith("#/"):
        return None
    node: Any = spec
    for part in ref[2:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def has_examples(media_obj: dict[str, Any]) -> bool:
    if "example" in media_obj:
        return True
    examples = media_obj.get("examples")
    if isinstance(examples, dict) and examples:
        return True
    schema = media_obj.get("schema")
    if isinstance(schema, dict) and ("example" in schema or (isinstance(schema.get("examples"), list) and schema.get("examples"))):
        return True
    return False


def review_operation(spec: dict[str, Any], operation: dict[str, Any], route_path: str, method_lower: str) -> list[Issue]:
    issues: list[Issue] = []

    def add(severity: str, pointer: str, message: str, suggestion: str | None = None) -> None:
        issues.append(Issue(severity=severity, pointer=pointer, message=message, suggestion=suggestion))

    op_base = ("paths", route_path, method_lower)

    summary = operation.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        add(
            "critical",
            join_pointer(*op_base, "summary"),
            "Missing operation summary.",
            "Add a short, specific summary (imperative verb + object).",
        )

    operation_id = operation.get("operationId")
    if not isinstance(operation_id, str) or not operation_id.strip():
        add(
            "critical",
            join_pointer(*op_base, "operationId"),
            "Missing operationId.",
            "Add a unique, stable operationId (used for SDKs and doc deep-linking).",
        )

    description = operation.get("description")
    if not isinstance(description, str) or not description.strip():
        add(
            "recommended",
            join_pointer(*op_base, "description"),
            "Missing operation description.",
            "Explain what the endpoint does, when to use it, and any prerequisites.",
        )

    tags = operation.get("tags")
    if not isinstance(tags, list) or not tags:
        add(
            "recommended",
            join_pointer(*op_base, "tags"),
            "Missing tags.",
            "Add at least one tag and keep tag values consistent across the spec.",
        )

    responses = operation.get("responses")
    if not isinstance(responses, dict) or not responses:
        add(
            "critical",
            join_pointer(*op_base, "responses"),
            "Missing responses object.",
            "Add at least one success response and common error responses.",
        )
        return issues

    success_keys = [k for k in responses.keys() if re.match(r"^2(\d\d|XX)$", str(k))]
    if not success_keys:
        add(
            "critical",
            join_pointer(*op_base, "responses"),
            "No success (2xx) response documented.",
            "Add a 2xx response (e.g., 200/201/204) with a clear description and schema (if applicable).",
        )

    for code, resp in responses.items():
        if not isinstance(resp, dict):
            add("critical", join_pointer(*op_base, "responses", str(code)), "Response value must be an object.")
            continue

        desc = resp.get("description")
        if not isinstance(desc, str) or not desc.strip():
            add(
                "critical",
                join_pointer(*op_base, "responses", str(code), "description"),
                f"Response {code} is missing a description.",
                "Add a short description that explains what this response means.",
            )

        # 204 typically has no response body.
        if str(code) == "204":
            continue

        content = resp.get("content")
        if content is None:
            add(
                "recommended",
                join_pointer(*op_base, "responses", str(code), "content"),
                f"Response {code} has no content section.",
                "If this response includes a body, add a content schema (and examples if possible).",
            )
            continue

        if not isinstance(content, dict) or not content:
            add(
                "recommended",
                join_pointer(*op_base, "responses", str(code), "content"),
                f"Response {code} content is empty or invalid.",
                "Add a media type (usually application/json) with a schema.",
            )
            continue

        for media_type, media_obj in content.items():
            if not isinstance(media_obj, dict):
                add(
                    "critical",
                    join_pointer(*op_base, "responses", str(code), "content", str(media_type)),
                    f"Response {code} content for {media_type} must be an object.",
                )
                continue

            schema = media_obj.get("schema")
            if not isinstance(schema, dict) or not schema:
                add(
                    "critical",
                    join_pointer(*op_base, "responses", str(code), "content", str(media_type), "schema"),
                    f"Response {code} content for {media_type} is missing a schema.",
                    "Add a schema (prefer $ref into components/schemas).",
                )

            if not has_examples(media_obj):
                add(
                    "recommended",
                    join_pointer(*op_base, "responses", str(code), "content", str(media_type)),
                    f"Response {code} content for {media_type} has no examples.",
                    "Add an example or examples for a typical response payload.",
                )

    # Parameters
    parameters = operation.get("parameters")
    if isinstance(parameters, list):
        for index, parameter in enumerate(parameters):
            if not isinstance(parameter, dict):
                continue
            desc = parameter.get("description")
            if not isinstance(desc, str) or not desc.strip():
                add(
                    "recommended",
                    join_pointer(*op_base, "parameters", str(index), "description"),
                    "Parameter is missing a description.",
                    "Explain what the parameter does and include format/constraints if relevant.",
                )

            schema = parameter.get("schema")
            if not isinstance(schema, dict) or not schema:
                add(
                    "recommended",
                    join_pointer(*op_base, "parameters", str(index), "schema"),
                    "Parameter is missing a schema.",
                    "Add a schema with type/format/constraints (or $ref).",
                )

    # Request body
    request_body = operation.get("requestBody")
    if isinstance(request_body, dict):
        content = request_body.get("content")
        if not isinstance(content, dict) or not content:
            add(
                "recommended",
                join_pointer(*op_base, "requestBody", "content"),
                "requestBody.content is missing or empty.",
                "Add at least one media type with a schema (usually application/json).",
            )
        else:
            for media_type, media_obj in content.items():
                if not isinstance(media_obj, dict):
                    continue
                schema = media_obj.get("schema")
                if not isinstance(schema, dict) or not schema:
                    add(
                        "recommended",
                        join_pointer(*op_base, "requestBody", "content", str(media_type), "schema"),
                        f"requestBody content for {media_type} is missing a schema.",
                        "Add a schema. For complex bodies (>5 fields), prefer a $ref into components/schemas.",
                    )
                    continue

                if not has_examples(media_obj):
                    add(
                        "recommended",
                        join_pointer(*op_base, "requestBody", "content", str(media_type)),
                        f"requestBody content for {media_type} has no examples.",
                        "Add an example or examples for a typical request payload.",
                    )

                if "$ref" not in schema:
                    properties = schema.get("properties") if isinstance(schema, dict) else None
                    if isinstance(properties, dict) and len(properties) > 5:
                        add(
                            "recommended",
                            join_pointer(*op_base, "requestBody", "content", str(media_type), "schema"),
                            f"requestBody schema for {media_type} is a large inline object ({len(properties)} fields).",
                            "Move this schema to components/schemas and reference it with $ref.",
                        )

    # Schema docs (only check local refs and only a shallow set; keep noise low)
    referenced_refs: set[str] = set()
    for schema_ref in iter_schema_refs(operation):
        if schema_ref.startswith("#/components/schemas/"):
            referenced_refs.add(schema_ref)

    for schema_ref in sorted(referenced_refs):
        schema_obj = resolve_ref(spec, schema_ref)
        if not isinstance(schema_obj, dict):
            continue
        schema_name = schema_ref.split("/")[-1]
        schema_pointer = ("components", "schemas", schema_name)

        schema_desc = schema_obj.get("description")
        if not isinstance(schema_desc, str) or not schema_desc.strip():
            add(
                "recommended",
                join_pointer(*schema_pointer, "description"),
                f"Schema '{schema_name}' is missing a description.",
                "Add a one-paragraph description of what this schema represents.",
            )

        properties = schema_obj.get("properties")
        if isinstance(properties, dict) and properties:
            for prop_name, prop_obj in properties.items():
                if not isinstance(prop_obj, dict):
                    continue
                prop_desc = prop_obj.get("description")
                if not isinstance(prop_desc, str) or not prop_desc.strip():
                    add(
                        "minor",
                        join_pointer(*schema_pointer, "properties", str(prop_name), "description"),
                        f"Property '{schema_name}.{prop_name}' is missing a description.",
                        "Add a short description that clarifies semantics and expected format.",
                    )

    return issues


def issues_to_markdown(ref: OperationRef, operation_id: str | None, issues: list[Issue]) -> str:
    by_severity: dict[str, list[Issue]] = {"critical": [], "recommended": [], "minor": []}
    for issue in issues:
        by_severity.setdefault(issue.severity, []).append(issue)

    lines: list[str] = []
    lines.append("## OpenAPI operation review")
    lines.append("")
    lines.append(f"- Spec: `{ref.spec_path.as_posix()}`")
    lines.append(f"- Operation: `{ref.method} {ref.route_path}`")
    if operation_id:
        lines.append(f"- operationId: `{operation_id}`")
    lines.append(f"- Source: {ref.source}")
    lines.append("")

    for severity, title in [("critical", "Critical"), ("recommended", "Recommended"), ("minor", "Minor")]:
        items = by_severity.get(severity, [])
        lines.append(f"### {title}")
        if not items:
            lines.append("- None")
            lines.append("")
            continue

        for item in items:
            suggestion = f" Suggested fix: {item.suggestion}" if item.suggestion else ""
            lines.append(f"- `{item.pointer}`: {item.message}{suggestion}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mdx", type=str, help="Path to an endpoint MDX file with frontmatter openapi: '<spec> <METHOD> <PATH>'")
    parser.add_argument("--spec", type=str, help="Path to openapi.json (relative to repo root or CWD)")
    parser.add_argument("--method", type=str, help="HTTP method (GET/POST/...)")
    parser.add_argument("--path", dest="route_path", type=str, help="Route path (e.g., /gst/compliance/...)")
    args = parser.parse_args()

    if bool(args.mdx) == bool(args.spec):
        print("Provide exactly one of: --mdx OR --spec/--method/--path.", file=sys.stderr)
        return 2

    repo_root = Path.cwd().resolve()

    if args.mdx:
        mdx_path = Path(args.mdx)
        repo_root = find_repo_root(mdx_path)
        openapi_value = parse_mdx_openapi_value(mdx_path)
        spec_ref, method, route_path = parse_openapi_ref(openapi_value)
        spec_path = repo_root / spec_ref.lstrip("/")
        ref = OperationRef(
            spec_path=spec_path,
            method=method.upper(),
            route_path=route_path,
            source=f"mdx:{mdx_path.as_posix()} (openapi: {openapi_value})",
        )
    else:
        spec_path = Path(args.spec)
        if not spec_path.is_absolute():
            spec_path = repo_root / spec_path
        ref = OperationRef(
            spec_path=spec_path.resolve(),
            method=str(args.method or "").upper(),
            route_path=str(args.route_path or ""),
            source="cli:--spec/--method/--path",
        )

    if not ref.method or not ref.route_path:
        print("Missing --method and/or --path.", file=sys.stderr)
        return 2

    spec = load_json(ref.spec_path)
    operation, route_path, method_lower = get_operation(spec, ref.method, ref.route_path)
    operation_id = operation.get("operationId") if isinstance(operation.get("operationId"), str) else None
    issues = review_operation(spec, operation, route_path, method_lower)

    report = issues_to_markdown(ref, operation_id, issues)
    print(report)

    if any(issue.severity == "critical" for issue in issues):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
