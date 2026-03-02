# prepare_data_for_pricing - 最小执行流程

## Step 0: 探测 + 下载

```bash
cd /hdd/hdd9/jrzhang
/home/jrzhang/miniconda3/bin/python .github/skills/prepare_data_for_pricing/scripts/10_probe_uqer_api.py
/home/jrzhang/miniconda3/bin/python .github/skills/prepare_data_for_pricing/scripts/20_download_minimal_samples.py
```

## Step 1: 建库建表

```bash
/home/jrzhang/miniconda3/bin/python .github/skills/execute-dlang/scripts/ddb_runner/execute.py \
  .github/skills/prepare_data_for_pricing/scripts/30_create_pricing_schema.dos \
  --host 127.0.0.1 --port 8848 --user admin --password 123456
```

## Step 2: 导入样本

```bash
/home/jrzhang/miniconda3/bin/python .github/skills/prepare_data_for_pricing/scripts/40_ingest_raw_to_ddb.py
```

## Step 3: 运行 Case1 / Case2

```bash
/home/jrzhang/miniconda3/bin/python .github/skills/execute-dlang/scripts/ddb_runner/execute.py \
  .github/skills/prepare_data_for_pricing/scripts/50_run_case1_irs_pricing.dos \
  --host 127.0.0.1 --port 8848 --user admin --password 123456

/home/jrzhang/miniconda3/bin/python .github/skills/execute-dlang/scripts/ddb_runner/execute.py \
  .github/skills/prepare_data_for_pricing/scripts/60_run_case2_curve_bootstrap.dos \
  --host 127.0.0.1 --port 8848 --user admin --password 123456
```

## Step 4: 生成标准报告

```bash
/home/jrzhang/miniconda3/bin/python .github/skills/prepare_data_for_pricing/scripts/70_generate_standard_report.py
```
