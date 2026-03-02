# 生成单页网页报告

本层只负责报告渲染，复用通用技能：`.github/skills/factor-eval-web-report`。

```powershell
python .github/skills/factor-eval-web-report/scripts/generate_single_page_report.py --input .github/skills/research-ddb/outputs/average_monthly_dazzling_volatility_metrics.json --out .github/skills/research-ddb/outputs/average_monthly_dazzling_volatility_report.html
```

```powershell
cd .github/skills/research-ddb/outputs
python -m http.server 8765
```

访问：

`http://127.0.0.1:8765/average_monthly_dazzling_volatility_report.html`
