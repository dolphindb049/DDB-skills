from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate multi-factor analysis pack: cards + ddb code + catalog")
    parser.add_argument("--text", required=True, help="Extracted report text file")
    parser.add_argument("--factor-spec", required=True, help="JSON file containing factor definitions")
    parser.add_argument("--outdir", required=True, help="Output directory")
    return parser.parse_args()


def default_logic(text: str) -> str:
    if "投资要点" in text:
        return text.split("投资要点", 1)[-1][:900].strip()
    return "请补充金融逻辑摘要。"


def build_card(factor: dict, fallback_logic: str) -> str:
    name = factor["name"]
    description = factor.get("description", fallback_logic)
    formula = factor.get("formula", "请填写数学公式")
    variables = factor.get("variables", [])
    boundary = factor.get("boundary", ["缺失值处理", "除零处理", "极值处理"])

    lines = [
        f"# 因子卡片：{name}",
        "",
        "## 因子描述",
        description,
        "",
        "## 数学公式",
        "$$",
        formula,
        "$$",
        "",
        "## 变量定义",
    ]
    if variables:
        for item in variables:
            lines.append(f"- {item.get('name', 'var')}: {item.get('meaning', '')}")
    else:
        lines.append("- 请补充变量定义")

    lines.extend(["", "## 边界处理"])
    for b in boundary:
        lines.append(f"- {b}")

    lines.extend(["", "## DolphinDB 代码", "```dolphindb"])
    lines.append(factor.get("ddb_code", "// TODO: add dolphindb script"))
    lines.extend(["```", ""])
    return "\n".join(lines)


def normalize_ddb_code(name: str, ddb_code: str) -> str:
    if ddb_code.strip():
        return ddb_code
    return (
        f"// Auto template for {name}\n"
        f"src = loadTable(\"dfs://stock_daily\", \"stock_daily_prev\")\n"
        f"res = select ts_code as securityid, trade_date, 0.0 as factor_value from src\n"
        f"res = select securityid, trade_date, `{name} as factor_name, factor_value from res\n"
        f"res"
    )


def main() -> None:
    args = parse_args()
    text = Path(args.text).read_text(encoding="utf-8", errors="ignore")
    spec = json.loads(Path(args.factor_spec).read_text(encoding="utf-8"))
    factors = spec.get("factors", [])

    outdir = Path(args.outdir)
    cards_dir = outdir / "factor_cards"
    scripts_dir = outdir / "ddb_scripts"
    cards_dir.mkdir(parents=True, exist_ok=True)
    scripts_dir.mkdir(parents=True, exist_ok=True)

    fallback = default_logic(text)
    catalog = {"factors": []}

    for factor in factors:
        name = factor["name"]
        card = build_card(factor, fallback)
        card_path = cards_dir / f"{name}.md"
        card_path.write_text(card, encoding="utf-8")

        ddb = normalize_ddb_code(name, factor.get("ddb_code", ""))
        dos_path = scripts_dir / f"{name}.dos"
        dos_path.write_text(ddb, encoding="utf-8")

        catalog["factors"].append(
            {
                "name": name,
                "description": factor.get("description", ""),
                "formula": factor.get("formula", ""),
                "card": str(card_path),
                "ddb_script": str(dos_path),
            }
        )

    catalog_path = outdir / "factor_catalog.json"
    catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"generated factors: {len(catalog['factors'])}")
    print(f"catalog: {catalog_path}")


if __name__ == "__main__":
    main()
