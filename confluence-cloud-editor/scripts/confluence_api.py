#!/usr/bin/env python3
import argparse
import base64
import html
import json
import mimetypes
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"").strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise SystemExit(f"Missing required env var: {name}")
    return value


class ConfluenceClient:
    def __init__(self, base_url: str, email: str, token: str) -> None:
        self.base_url = base_url.rstrip("/")
        auth_raw = f"{email}:{token}".encode("utf-8")
        self.auth_header = "Basic " + base64.b64encode(auth_raw).decode("ascii")

    def _request(self, method: str, path: str, payload=None):
        url = path if path.startswith("http") else f"{self.base_url}{path}"
        cmd = [
            "curl",
            "-sS",
            "--fail-with-body",
            "-X",
            method,
            url,
            "-H",
            f"Authorization: {self.auth_header}",
            "-H",
            "Accept: application/json",
        ]
        if payload is not None:
            cmd.extend(["-H", "Content-Type: application/json"])
            cmd.extend(["--data", json.dumps(payload, ensure_ascii=False)])
        try:
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as exc:
            msg = exc.stderr.strip() or exc.stdout.strip() or str(exc)
            raise SystemExit(f"Request failed: {msg}") from exc
        body = result.stdout.strip()
        return json.loads(body) if body else {}

    def auth_test(self):
        return self._request("GET", "/rest/api/space?limit=1")

    def get_page(self, page_id: str):
        params = urllib.parse.urlencode({"expand": "body.storage,version,title"})
        return self._request("GET", f"/rest/api/content/{page_id}?{params}")

    def get_page_with_meta(self, page_id: str):
        params = urllib.parse.urlencode({"expand": "body.storage,version,title,type,space"})
        return self._request("GET", f"/rest/api/content/{page_id}?{params}")

    def list_children(self, page_id: str, recursive: bool = False):
        queue = [page_id]
        seen = set()
        rows = []

        while queue:
            current = queue.pop(0)
            if current in seen:
                continue
            seen.add(current)

            next_path = f"/rest/api/content/{current}/child/page?limit=50"
            while next_path:
                data = self._request("GET", next_path)
                for item in data.get("results", []):
                    child_id = item.get("id", "")
                    title = item.get("title", "")
                    rows.append({"parent_id": current, "id": child_id, "title": title})
                    if recursive and child_id:
                        queue.append(child_id)

                next_link = data.get("_links", {}).get("next")
                next_path = next_link if next_link else ""

        return rows

    def update_page_storage(self, page_id: str, new_storage_value: str):
        page = self.get_page(page_id)
        current_version = int(page["version"]["number"])
        payload = {
            "id": page["id"],
            "type": page.get("type", "page"),
            "title": page["title"],
            "version": {"number": current_version + 1},
            "body": {
                "storage": {
                    "value": new_storage_value,
                    "representation": "storage",
                }
            },
        }
        return self._request("PUT", f"/rest/api/content/{page_id}", payload=payload)

    def list_page_comments(self, page_id: str):
        return self._request(
            "GET",
            f"/rest/api/content/{page_id}/child/comment?expand=body.storage,version&limit=200",
        )

    def delete_content(self, content_id: str):
        return self._request("DELETE", f"/rest/api/content/{content_id}")

    def create_page_storage(
        self, title: str, space_key: str, storage_value: str, parent_id: str = ""
    ):
        payload = {
            "type": "page",
            "title": title,
            "space": {"key": space_key},
            "body": {
                "storage": {
                    "value": storage_value,
                    "representation": "storage",
                }
            },
        }
        if parent_id:
            payload["ancestors"] = [{"id": parent_id}]
        return self._request("POST", "/rest/api/content", payload=payload)

    def upload_attachment(self, page_id: str, file_path: Path):
        url = f"{self.base_url}/rest/api/content/{page_id}/child/attachment"
        content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        boundary = "----ConfluenceBoundary" + uuid.uuid4().hex

        head = (
            f"--{boundary}\r\n"
            f"Content-Disposition: form-data; name=\"file\"; filename=\"{file_path.name}\"\r\n"
            f"Content-Type: {content_type}\r\n\r\n"
        ).encode("utf-8")
        tail = f"\r\n--{boundary}--\r\n".encode("utf-8")
        body = head + file_path.read_bytes() + tail

        req = urllib.request.Request(url, data=body, method="POST")
        req.add_header("Authorization", self.auth_header)
        req.add_header("Accept", "application/json")
        req.add_header("X-Atlassian-Token", "no-check")
        req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            if exc.code == 400 and "same file name as an existing attachment" in detail:
                return {
                    "skipped": True,
                    "reason": "duplicate_filename",
                    "filename": file_path.name,
                }
            raise SystemExit(
                f"Attachment upload failed for {file_path}: HTTP {exc.code} {detail}"
            ) from exc


def slugify(value: str) -> str:
    # Keep file names portable and readable.
    val = re.sub(r"\s+", "-", value.strip())
    val = re.sub(r"[^\w\-.]", "-", val, flags=re.UNICODE)
    val = re.sub(r"-{2,}", "-", val).strip("-")
    return val or "untitled"


def webui_to_url(base_url: str, webui: str) -> str:
    if not webui:
        return ""
    if webui.startswith("http://") or webui.startswith("https://"):
        return webui
    if "/wiki" in base_url:
        return base_url.split("/wiki", 1)[0] + webui
    return base_url.rstrip("/") + webui


def auto_link_plain_urls(value: str) -> str:
    return re.sub(r"(?<![\">])(https?://[^\s<]+)", r'<a href="\1">\1</a>', value)


def format_inline_markdown(value: str) -> str:
    escaped = html.escape(value, quote=False)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    escaped = re.sub(
        r"\[(.*?)\]\((https?://[^)]+)\)",
        r'<a href="\2">\1</a>',
        escaped,
    )
    escaped = auto_link_plain_urls(escaped)
    return escaped


def markdown_to_storage_html(md_text: str, md_base_dir: Path, image_width: int = 900):
    lines = md_text.splitlines()
    html_parts = []
    attachment_paths = []
    seen_attachments = set()
    in_ul = False
    in_ol = False

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            html_parts.append("</ul>")
            in_ul = False
        if in_ol:
            html_parts.append("</ol>")
            in_ol = False

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            close_lists()
            continue

        image_inline = re.search(r"!\[[^\]]*\]\(([^)]+)\)", line)
        if image_inline:
            close_lists()
            prefix = line[: image_inline.start()].strip()
            suffix = line[image_inline.end() :].strip()
            image_ref = image_inline.group(1).strip()

            if prefix:
                html_parts.append(f"<p>{format_inline_markdown(prefix)}</p>")

            if re.match(r"^https?://", image_ref):
                html_parts.append(
                    f'<p><ac:image ac:width="{image_width}"><ri:url ri:value="{html.escape(image_ref, quote=True)}" /></ac:image></p>'
                )
            else:
                image_path = (md_base_dir / image_ref).resolve()
                if not image_path.exists():
                    raise SystemExit(f"Image file not found: {image_path}")
                if image_path not in seen_attachments:
                    attachment_paths.append(image_path)
                    seen_attachments.add(image_path)
                html_parts.append(
                    f'<p><ac:image ac:width="{image_width}"><ri:attachment ri:filename="{html.escape(image_path.name, quote=True)}" /></ac:image></p>'
                )

            if suffix:
                html_parts.append(f"<p>{format_inline_markdown(suffix)}</p>")
            continue

        if line.startswith("# "):
            close_lists()
            html_parts.append(f"<h1>{format_inline_markdown(line[2:].strip())}</h1>")
            continue
        if line.startswith("## "):
            close_lists()
            html_parts.append(f"<h2>{format_inline_markdown(line[3:].strip())}</h2>")
            continue
        if line.startswith("### "):
            close_lists()
            html_parts.append(f"<h3>{format_inline_markdown(line[4:].strip())}</h3>")
            continue
        if line.strip() == "---":
            close_lists()
            html_parts.append("<hr/>")
            continue
        if line.startswith("- "):
            if in_ol:
                html_parts.append("</ol>")
                in_ol = False
            if not in_ul:
                html_parts.append("<ul>")
                in_ul = True
            html_parts.append(f"<li>{format_inline_markdown(line[2:].strip())}</li>")
            continue

        ordered = re.match(r"^(\d+)\.\s+(.*)$", line)
        if ordered:
            if in_ul:
                html_parts.append("</ul>")
                in_ul = False
            if not in_ol:
                html_parts.append("<ol>")
                in_ol = True
            html_parts.append(f"<li>{format_inline_markdown(ordered.group(2).strip())}</li>")
            continue

        close_lists()
        html_parts.append(f"<p>{format_inline_markdown(line.strip())}</p>")

    close_lists()
    return "\n".join(html_parts), attachment_paths


def cmd_auth_test(client: ConfluenceClient, _args):
    data = client.auth_test()
    results = data.get("results", [])
    first = results[0] if results else {}
    print(
        json.dumps(
            {
                "ok": True,
                "space_count": data.get("size", 0),
                "first_space_key": first.get("key"),
                "first_space_name": first.get("name"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def cmd_get_page(client: ConfluenceClient, args):
    page = client.get_page(args.page_id)
    print(
        json.dumps(
            {
                "id": page.get("id"),
                "title": page.get("title"),
                "version": page.get("version", {}).get("number"),
                "webui": page.get("_links", {}).get("webui"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def cmd_list_children(client: ConfluenceClient, args):
    rows = client.list_children(args.page_id, recursive=args.recursive)
    print(json.dumps({"count": len(rows), "children": rows}, ensure_ascii=False, indent=2))


def cmd_append_note(client: ConfluenceClient, args):
    page = client.get_page(args.page_id)
    storage = page.get("body", {}).get("storage", {}).get("value", "")
    if not storage:
        raise SystemExit("Page body.storage.value is empty; aborting.")

    note_html = f"<p><em>{args.note}</em></p>"
    new_storage = storage + "\n" + note_html

    if args.dry_run:
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "page_id": args.page_id,
                    "title": page.get("title"),
                    "current_version": page.get("version", {}).get("number"),
                    "appended_note": args.note,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    updated = client.update_page_storage(args.page_id, new_storage)
    print(
        json.dumps(
            {
                "updated": True,
                "id": updated.get("id"),
                "title": updated.get("title"),
                "new_version": updated.get("version", {}).get("number"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def cmd_append_note_tree(client: ConfluenceClient, args):
    rows = client.list_children(args.page_id, recursive=True)
    page_ids = [args.page_id] + [r["id"] for r in rows if r.get("id")]
    if args.max_pages > 0:
        page_ids = page_ids[: args.max_pages]

    if args.dry_run:
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "target_count": len(page_ids),
                    "target_page_ids": page_ids,
                    "note": args.note,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    results = []
    for page_id in page_ids:
        page = client.get_page(page_id)
        storage = page.get("body", {}).get("storage", {}).get("value", "")
        if not storage:
            results.append({"id": page_id, "updated": False, "reason": "empty body"})
            continue
        note_html = f"<p><em>{args.note}</em></p>"
        new_storage = storage + "\n" + note_html
        updated = client.update_page_storage(page_id, new_storage)
        results.append(
            {
                "id": updated.get("id", page_id),
                "title": updated.get("title"),
                "updated": True,
                "new_version": updated.get("version", {}).get("number"),
            }
        )

    print(
        json.dumps(
            {
                "updated_count": sum(1 for r in results if r.get("updated")),
                "total": len(results),
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def cmd_add_comment(client: ConfluenceClient, args):
    payload = {
        "type": "comment",
        "container": {"type": "page", "id": args.page_id},
        "body": {
            "storage": {
                "value": f"<p>{args.text}</p>",
                "representation": "storage",
            }
        },
    }
    if args.dry_run:
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "page_id": args.page_id,
                    "text": args.text,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return
    data = client._request("POST", "/rest/api/content", payload=payload)
    print(
        json.dumps(
            {
                "created": True,
                "comment_id": data.get("id"),
                "page_id": args.page_id,
                "version": data.get("version", {}).get("number"),
                "webui": data.get("_links", {}).get("webui"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def cmd_add_comment_tree(client: ConfluenceClient, args):
    rows = client.list_children(args.page_id, recursive=True)
    page_ids = [args.page_id] + [r["id"] for r in rows if r.get("id")]
    if args.max_pages > 0:
        page_ids = page_ids[: args.max_pages]

    if args.dry_run:
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "target_count": len(page_ids),
                    "target_page_ids": page_ids,
                    "text": args.text,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    results = []
    for page_id in page_ids:
        payload = {
            "type": "comment",
            "container": {"type": "page", "id": page_id},
            "body": {
                "storage": {
                    "value": f"<p>{args.text}</p>",
                    "representation": "storage",
                }
            },
        }
        data = client._request("POST", "/rest/api/content", payload=payload)
        results.append(
            {
                "page_id": page_id,
                "comment_id": data.get("id"),
                "webui": data.get("_links", {}).get("webui"),
                "created": True,
            }
        )

    print(
        json.dumps(
            {
                "created_count": len(results),
                "total": len(results),
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def cmd_add_inline_comment(client: ConfluenceClient, args):
    page = client.get_page(args.page_id)
    storage = page.get("body", {}).get("storage", {}).get("value", "")
    if not storage:
        raise SystemExit("Page body.storage.value is empty; cannot create inline comment.")

    match_count = storage.count(args.selection)
    if match_count <= 0:
        raise SystemExit(f'Selection text not found in page body: "{args.selection}"')
    if args.match_index < 0 or args.match_index >= match_count:
        raise SystemExit(
            f"Invalid --match-index {args.match_index}; valid range: 0..{match_count - 1}"
        )

    payload = {
        "pageId": args.page_id,
        "body": {
            "representation": "storage",
            "value": f"<p>{args.text}</p>",
        },
        "inlineCommentProperties": {
            "textSelection": args.selection,
            "textSelectionMatchCount": match_count,
            "textSelectionMatchIndex": args.match_index,
        },
    }

    if args.dry_run:
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "page_id": args.page_id,
                    "selection": args.selection,
                    "selection_match_count": match_count,
                    "selection_match_index": args.match_index,
                    "text": args.text,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    data = client._request("POST", "/api/v2/inline-comments", payload=payload)
    print(
        json.dumps(
            {
                "created": True,
                "comment_id": data.get("id"),
                "page_id": data.get("pageId"),
                "selection": args.selection,
                "selection_match_count": match_count,
                "selection_match_index": args.match_index,
                "webui": data.get("_links", {}).get("webui"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def cmd_list_comments(client: ConfluenceClient, args):
    data = client.list_page_comments(args.page_id)
    rows = []
    for it in data.get("results", []):
        body_value = it.get("body", {}).get("storage", {}).get("value", "")
        if args.contains and args.contains not in body_value:
            continue
        rows.append(
            {
                "id": it.get("id"),
                "title": it.get("title"),
                "version": it.get("version", {}).get("number"),
                "webui": it.get("_links", {}).get("webui"),
                "preview": body_value[:120],
            }
        )
    print(json.dumps({"count": len(rows), "comments": rows}, ensure_ascii=False, indent=2))


def cmd_delete_comment(client: ConfluenceClient, args):
    if args.dry_run:
        print(json.dumps({"dry_run": True, "comment_id": args.comment_id}, ensure_ascii=False, indent=2))
        return
    client.delete_content(args.comment_id)
    print(json.dumps({"deleted": True, "comment_id": args.comment_id}, ensure_ascii=False, indent=2))


def cmd_export_pages_md(client: ConfluenceClient, args):
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    targets = []
    if args.include_root:
        root_page = client.get_page(args.page_id)
        targets.append({"id": args.page_id, "title": root_page.get("title", "")})

    children = client.list_children(args.page_id, recursive=False)
    if args.title_prefix:
        children = [it for it in children if it.get("title", "").startswith(args.title_prefix)]
    if args.max_pages > 0:
        children = children[: args.max_pages]
    targets.extend(children)

    if not targets:
        raise SystemExit("No pages selected for export.")

    if args.dry_run:
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "selected_count": len(targets),
                    "page_ids": [it.get("id") for it in targets],
                    "out_dir": str(out_dir),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    manifest = []
    for idx, item in enumerate(targets, start=1):
        page_id = item.get("id")
        page = client.get_page(page_id)
        title = page.get("title", "")
        storage = page.get("body", {}).get("storage", {}).get("value", "")
        if not storage:
            manifest.append({"id": page_id, "title": title, "exported": False, "reason": "empty body"})
            continue

        try:
            md = subprocess.run(
                ["pandoc", "-f", "html", "-t", "gfm"],
                input=storage,
                text=True,
                capture_output=True,
                check=True,
            ).stdout
        except subprocess.CalledProcessError as exc:
            raise SystemExit(f"pandoc failed for page {page_id}: {exc.stderr.strip() or exc}") from exc

        webui = page.get("_links", {}).get("webui", "")
        source_url = webui_to_url(client.base_url, webui)
        header = (
            f"# {title}\n\n"
            f"- Confluence Page ID: `{page_id}`\n"
            f"- Source: {source_url}\n"
            f"- Exported At (UTC): {datetime.now(timezone.utc).isoformat()}\n\n"
            f"---\n\n"
        )
        file_name = f"{idx:02d}-{slugify(title)}-{page_id}.md"
        file_path = out_dir / file_name
        file_path.write_text(header + md.strip() + "\n", encoding="utf-8")
        manifest.append({"id": page_id, "title": title, "exported": True, "file": str(file_path)})

    print(
        json.dumps(
            {
                "exported_count": sum(1 for it in manifest if it.get("exported")),
                "total": len(manifest),
                "out_dir": str(out_dir),
                "pages": manifest,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def cmd_publish_md_page(client: ConfluenceClient, args):
    md_path = Path(args.md_file)
    if not md_path.exists():
        raise SystemExit(f"Markdown file not found: {md_path}")

    md_text = md_path.read_text(encoding="utf-8")
    storage_html, attachment_paths = markdown_to_storage_html(
        md_text=md_text,
        md_base_dir=md_path.parent,
        image_width=args.image_width,
    )

    if args.page_id:
        page = client.get_page_with_meta(args.page_id)
        title = args.title if args.title else page.get("title", "")
        payload = {
            "id": args.page_id,
            "type": page.get("type", "page"),
            "title": title,
            "version": {"number": int(page.get("version", {}).get("number", 1)) + 1},
            "body": {"storage": {"value": storage_html, "representation": "storage"}},
        }
        if args.parent_id:
            payload["ancestors"] = [{"id": args.parent_id}]
        if args.space_key:
            payload["space"] = {"key": args.space_key}
        target = (
            json.dumps(
                {
                    "mode": "update",
                    "page_id": args.page_id,
                    "title": title,
                    "attachments": [str(p) for p in attachment_paths],
                },
                ensure_ascii=False,
                indent=2,
            )
            if args.dry_run
            else client._request("PUT", f"/rest/api/content/{args.page_id}", payload=payload)
        )
    else:
        if not args.title or not args.space_key:
            raise SystemExit("Create mode requires --title and --space-key when --page-id is omitted.")
        target = (
            json.dumps(
                {
                    "mode": "create",
                    "title": args.title,
                    "space_key": args.space_key,
                    "parent_id": args.parent_id,
                    "attachments": [str(p) for p in attachment_paths],
                },
                ensure_ascii=False,
                indent=2,
            )
            if args.dry_run
            else client.create_page_storage(
                title=args.title,
                space_key=args.space_key,
                storage_value=storage_html,
                parent_id=args.parent_id,
            )
        )

    if args.dry_run:
        print(target)
        return

    page_id = target.get("id", "")
    uploaded = []
    for file_path in attachment_paths:
        data = client.upload_attachment(page_id=page_id, file_path=file_path)
        uploaded.append(
            {
                "file": str(file_path),
                "count": len(data.get("results", [])),
                "skipped": bool(data.get("skipped", False)),
                "reason": data.get("reason", ""),
            }
        )

    print(
        json.dumps(
            {
                "published": True,
                "page_id": page_id,
                "title": target.get("title"),
                "webui": webui_to_url(client.base_url, target.get("_links", {}).get("webui", "")),
                "attachment_uploads": uploaded,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def build_parser():
    parser = argparse.ArgumentParser(description="Confluence Cloud API helper")
    parser.add_argument(
        "--env-file",
        default=".github/skills/confluence-cloud-editor/.env",
        help="Path to env file (default: .github/skills/confluence-cloud-editor/.env)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("auth-test", help="Validate API auth")

    p_get = sub.add_parser("get-page", help="Get page metadata")
    p_get.add_argument("--page-id", required=True)

    p_children = sub.add_parser("list-children", help="List child pages")
    p_children.add_argument("--page-id", required=True)
    p_children.add_argument("--recursive", action="store_true")

    p_append = sub.add_parser("append-note", help="Append an italic note paragraph")
    p_append.add_argument("--page-id", required=True)
    p_append.add_argument("--note", required=True)
    p_append.add_argument("--dry-run", action="store_true")

    p_append_tree = sub.add_parser(
        "append-note-tree", help="Append note to root page and all descendant pages"
    )
    p_append_tree.add_argument("--page-id", required=True, help="Root page ID")
    p_append_tree.add_argument("--note", required=True)
    p_append_tree.add_argument("--max-pages", type=int, default=0)
    p_append_tree.add_argument("--dry-run", action="store_true")

    p_comment = sub.add_parser("add-comment", help="Add a page comment")
    p_comment.add_argument("--page-id", required=True)
    p_comment.add_argument("--text", required=True)
    p_comment.add_argument("--dry-run", action="store_true")

    p_comment_tree = sub.add_parser(
        "add-comment-tree", help="Add one comment to root page and all descendant pages"
    )
    p_comment_tree.add_argument("--page-id", required=True, help="Root page ID")
    p_comment_tree.add_argument("--text", required=True)
    p_comment_tree.add_argument("--max-pages", type=int, default=0)
    p_comment_tree.add_argument("--dry-run", action="store_true")

    p_inline = sub.add_parser("add-inline-comment", help="Add an inline (text-selection) comment")
    p_inline.add_argument("--page-id", required=True)
    p_inline.add_argument("--selection", required=True, help="Exact text selected in page body")
    p_inline.add_argument("--text", required=True, help="Comment body text")
    p_inline.add_argument(
        "--match-index",
        type=int,
        default=0,
        help="0-based index among all matches of --selection in page body",
    )
    p_inline.add_argument("--dry-run", action="store_true")

    p_list_comments = sub.add_parser("list-comments", help="List comments on a page")
    p_list_comments.add_argument("--page-id", required=True)
    p_list_comments.add_argument("--contains", default="")

    p_delete = sub.add_parser("delete-comment", help="Delete a comment by ID")
    p_delete.add_argument("--comment-id", required=True)
    p_delete.add_argument("--dry-run", action="store_true")

    p_export = sub.add_parser("export-pages-md", help="Export selected pages to Markdown files")
    p_export.add_argument("--page-id", required=True, help="Root page ID")
    p_export.add_argument("--out-dir", required=True, help="Output directory for markdown files")
    p_export.add_argument(
        "--title-prefix",
        default="",
        help="Only export direct child pages whose title starts with this prefix",
    )
    p_export.add_argument("--max-pages", type=int, default=0, help="Maximum number of direct child pages")
    p_export.add_argument("--include-root", action="store_true", help="Also export root page")
    p_export.add_argument("--dry-run", action="store_true")

    p_publish = sub.add_parser(
        "publish-md-page",
        help="Create/update a Confluence page from Markdown with auto-links and image attachments",
    )
    p_publish.add_argument("--md-file", required=True, help="Markdown file path")
    p_publish.add_argument(
        "--page-id",
        default="",
        help="Update existing page ID (omit for create mode)",
    )
    p_publish.add_argument("--title", default="", help="Page title (required in create mode)")
    p_publish.add_argument(
        "--space-key",
        default="",
        help="Confluence space key (required in create mode)",
    )
    p_publish.add_argument("--parent-id", default="", help="Optional parent page ID")
    p_publish.add_argument("--image-width", type=int, default=900, help="Default image width")
    p_publish.add_argument("--dry-run", action="store_true")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    env_path = Path(args.env_file)
    load_env_file(env_path)

    base_url = require_env("CONFLUENCE_BASE_URL")
    email = require_env("CONFLUENCE_EMAIL")
    token = require_env("CONFLUENCE_API_TOKEN")

    client = ConfluenceClient(base_url=base_url, email=email, token=token)

    commands = {
        "auth-test": cmd_auth_test,
        "get-page": cmd_get_page,
        "list-children": cmd_list_children,
        "append-note": cmd_append_note,
        "append-note-tree": cmd_append_note_tree,
        "add-comment": cmd_add_comment,
        "add-comment-tree": cmd_add_comment_tree,
        "add-inline-comment": cmd_add_inline_comment,
        "list-comments": cmd_list_comments,
        "delete-comment": cmd_delete_comment,
        "export-pages-md": cmd_export_pages_md,
        "publish-md-page": cmd_publish_md_page,
    }
    commands[args.command](client, args)


if __name__ == "__main__":
    main()
