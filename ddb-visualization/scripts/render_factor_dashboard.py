from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))

    summary = payload["summary"]
    desc = payload.get("desc_stats", [])
    ic = payload.get("ic_analysis", [])
    ret = payload.get("returns_analysis", [])

    html = f"""
<!doctype html>
<html>
<head>
  <meta charset='utf-8'/>
  <title>{summary['factor']} Dashboard</title>
  <script src='https://cdn.plot.ly/plotly-2.35.2.min.js'></script>
  <style>
    body {{font-family: Arial, sans-serif; margin: 24px;}}
    .kpi {{display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 14px;}}
    .card {{border: 1px solid #ddd; border-radius: 8px; padding: 10px;}}
    table {{border-collapse: collapse; width: 100%; margin: 12px 0;}}
    th, td {{border: 1px solid #ddd; padding: 8px; font-size: 13px;}}
    th {{background: #f5f5f5;}}
    .grid {{display:grid; grid-template-columns: 1fr 1fr; gap: 16px;}}
  </style>
</head>
<body>
  <h1>因子评价 Dashboard</h1>
  <div class='kpi'>
    <div class='card'><b>状态</b><br/>{summary['status']}</div>
    <div class='card'><b>因子</b><br/>{summary['factor']}</div>
    <div class='card'><b>起始</b><br/>{summary['start_date']}</div>
    <div class='card'><b>结束</b><br/>{summary['end_date']}</div>
  </div>

  <h2>分组统计</h2>
  <table>
    <thead><tr><th>Quantile</th><th>Min</th><th>Max</th><th>Std</th><th>Count</th><th>Pct</th></tr></thead>
    <tbody>
      {''.join([f"<tr><td>{r['factor_quantile']}</td><td>{r['min_value']}</td><td>{r['max_value']}</td><td>{r['std_value']}</td><td>{r['cnt']}</td><td>{r['pct']}</td></tr>" for r in desc])}
    </tbody>
  </table>

  <div class='grid'>
    <div id='ic' style='height:320px;'></div>
    <div id='spread' style='height:320px;'></div>
  </div>
  <div class='grid'>
    <div id='quantile_count' style='height:320px;'></div>
    <div id='quantile_std' style='height:320px;'></div>
  </div>

  <script>
    const ic = {json.dumps(ic)};
    Plotly.newPlot('ic', [{{
      x: ic.map(x=>x.horizon),
      y: ic.map(x=>x.IC_Mean),
      type:'bar', name:'IC_Mean'
    }}], {{title:'IC Mean by Horizon'}});

    const ret = {json.dumps(ret)};
    const spread = ret.find(x=>x.metric==='Mean_Period_Wise_Spread_bps');
    Plotly.newPlot('spread', [{{
      x:['1D','5D','10D'],
      y:[spread.forward_returns_1D, spread.forward_returns_5D, spread.forward_returns_10D],
      type:'bar', name:'Spread bps'
    }}], {{title:'Top-Bottom Spread (bps)'}});

    const desc = {json.dumps(desc)};
    Plotly.newPlot('quantile_count', [{{
      x: desc.map(d=>d.factor_quantile),
      y: desc.map(d=>d.cnt),
      type:'bar', name:'Count'
    }}], {{title:'Quantile Count'}});

    Plotly.newPlot('quantile_std', [{{
      x: desc.map(d=>d.factor_quantile),
      y: desc.map(d=>d.std_value),
      type:'scatter', mode:'lines+markers', name:'Std'
    }}], {{title:'Quantile Std'}});
  </script>
</body>
</html>
"""

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"dashboard generated: {out}")


if __name__ == "__main__":
    main()
