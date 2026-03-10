import pandas as pd
import os

# 1. 明确我们要输出到的产物目录
output_dir = r"d:\work\202603_202606_product\skills\csap\reference"

# ========================
# 处理 1：参数字段级别的映射
# ========================
param_path = os.path.join(output_dir, "parameter.csv")
with open(param_path, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

parsed_data = []
for i, line in enumerate(lines):
    line = line.strip()
    if not line: continue
    if i == 0: continue # Skip the header
    parts = line.split('\t')
    if len(parts) >= 2:
        parsed_data.append({'参数名称': parts[0].strip(), '参数含义': parts[1].strip()})
    else:
        parts = line.split(' ', 1)
        if len(parts) >= 2:
            parsed_data.append({'参数名称': parts[0].strip(), '参数含义': parts[1].strip()})

df_params = pd.DataFrame(parsed_data)

# A股字段对照字典
mapping_dict = {
    # 基础映射
    'gvkey': ('ts_code / wind_code', '股票/公司代码(主键)'),
    'permno': ('ts_code / wind_code', '股票代码(主键)'),
    'tic': ('sec_name', '股票简称'),
    'datadate': ('end_date', '报告期(最后一天)'),
    'time_avail_m': ('trade_date', '交易日期(通常按月或按日)'),
    'lpermno': ('ts_code', '股票代码'),
    'lpermco': ('ts_code', '股票代码'),
    'fyear': ('f_year', '财务会计年度'),
    
    # 市场行情量价
    'ret': ('pct_chg / 100', '股票多期/单期收益率估算(通常转小数)'),
    'prc': ('close', '收盘价(部分场景需判断是否前/后复权)'),
    'shrout': ('total_share / float_share', '总股本/流通股本'),
    'vol': ('vol', '成交量(手/股)'),
    'mve_c': ('total_mv / float_mv', '总市值或流通市值(随月更新)'),
    'me_datadate': ('total_mv', '总市值(对齐财报期)'),
    'ewretd': ('mkt_ret', '市场等权重收益率/全A指数收益率'),
    'vwretd': ('mkt_ret', '市场市值加权收益率/全A指数收益率'),
    'rf': ('risk_free_rate', '无风险利率(如一年期国债到期收益率)'),
    
    # 资产负债表
    'at': ('total_assets', '资产总计'),
    'atq': ('total_assets', '资产总计(季末)'),
    'lt': ('total_liab', '负债合计'),
    'ltq': ('total_liab', '负债合计(季末)'),
    'seq': ('total_hldr_eqy_exc_min_int', '归属母公司所有者权益合计'),
    'ceq': ('total_hldr_eqy_exc_min_int', '归属母公司所有者权益合计'),
    'ceqt': ('total_hldr_eqy_exc_min_int', '归属母公司所有者权益合计'),
    'act': ('total_cur_assets', '流动资产合计'),
    'lct': ('total_cur_liab', '流动负债合计'),
    'che': ('money_cap + tradable_fin_assets', '货币资金及部分交易性金融资产'),
    'cheq': ('money_cap + tradable_fin_assets', '货币资金(季度)'),
    'dlc': ('short_term_borr', '短期借款等直接一年内到期借款'),
    'dlcq': ('short_term_borr', '短期借款(季度)'),
    'dltt': ('long_term_borr', '长期借款'),
    'txp': ('taxes_payable', '应交税费'),
    'aco': ('notes_receiv + accounts_receiv', '应收票据及应收账款'),
    'invt': ('inventories', '存货'),
    'ppent': ('fix_assets', '固定资产净额'),
    'intan': ('intan_assets', '无形资产净额'),
    'pstk': ('oth_eqt_tools_p_shr', '优先股'),
    'pstkrv': ('oth_eqt_tools_p_shr', '优先股(可赎回)'),
    'pstkl': ('oth_eqt_tools_p_shr', '优先股(清算值)'),
    'txditc': ('defer_tax_liab', '递延所得税负债及投资税收抵免'),
    'prba': ('pension_liab', '设定受益计划净负债/应付职工薪酬(长期)'),
    'mia': ('minority_int', '少数股东权益'),
    
    # 利润表
    'ni': ('n_income_attr_p', '归属母公司净利润(年化)'),
    'niq': ('n_income_attr_p', '归属母公司净利润(季度)'),
    'ib': ('n_income_attr_p', '净利润'),
    'ibq': ('n_income_attr_p', '净利润(季度)'),
    'revt': ('revenue', '营业收入'),
    'cogs': ('oper_cost', '营业成本'),
    'xrd': ('rd_exp', '研发费用'),
    'xad': ('sell_exp', 'A股无单列广告费时一律使用销售费用'),
    'xint': ('int_exp', '利息支出(一般在财务费用内)'),
    'xsga': ('sell_exp + admin_exp', '销售与管理费用总计'),
    'dp': ('depr_fa_coga_dpba', '折旧与摊销'),
    'ebitda': ('ebitda', '息税折旧摊销前利润'),

    # 现金流量表
    'oancf': ('net_cash_flows_oper_act', '经营活动产生的现金流量净额'),
    'ivncf': ('net_cash_flows_inv_act', '投资活动产生的现金流量净额'),
    'fincf': ('net_cash_flows_fnc_act', '筹资活动产生的现金流量净额'),
    'dvt': ('cash_div_dcl', '分配股利、利润或偿付利息支付的现金'),
    'capx': ('cash_pay_acq_const_fiolta', '购建固定资产无形资产等的现金支出(资本支出)'),
    'sstk': ('cash_recp_cap_contrib', '吸收投资收到的现金'),
    'prstkcc': ('cash_pay_dist_dpcp_int_exp', '支付其他与筹资有关的现金'),
}

def map_ashare_field(row):
    key = str(row['参数名称']).strip()
    if key in mapping_dict:
        return mapping_dict[key][0]
    return '待人工评估'

def map_ashare_desc(row):
    key = str(row['参数名称']).strip()
    if key in mapping_dict:
        return mapping_dict[key][1]
    return ''

df_params['A股映射字段名'] = df_params.apply(map_ashare_field, axis=1)
df_params['A股映射字段说明'] = df_params.apply(map_ashare_desc, axis=1)

# 保存最终给客户的交付 CSV
out_param_path = os.path.join(output_dir, "AShare_Parameter_Delivery.csv")
df_params.to_csv(out_param_path, index=False, encoding='utf-8-sig')


# ========================
# 处理 2：数据表的 A股映射逻辑 
# ========================
table_mappings = [
    {"美股原始表名": "monthlyCRSP", "A股建议对标表": "A股月度行情表 (Monthly_Quote)", "A股相关数据源表": "Wind_AShareEODPrices / Tushare_monthly", "核心用途": "作为因子核心主表，含收盘价、收益率、市值、换手率等估计算法参数"},
    {"美股原始表名": "dailyFF", "A股建议对标表": "A股日频五因子/三因子表 (FF_Daily)", "A股相关数据源表": "锐思(RESSET)五因子 / Tushare自建计算", "核心用途": "含有 SMB, HML 收益率和日度风险回报 (rf) 用于计算股票暴露Beta"},
    {"美股原始表名": "monthlyFF", "A股建议对标表": "A股月频五因子表 (FF_Monthly)", "A股相关数据源表": "锐思(RESSET)五因子 / 个股汇总", "核心用途": "回归计算长期风险因子的 Beta 用，等同 dailyFF"},
    {"美股原始表名": "monthlyMarket", "A股建议对标表": "A股宽基指数月度行情表 (Index_Monthly)", "A股相关数据源表": "万得全A(881001.WI) 行情数据", "核心用途": "获取全市场收益率以用来对标Beta与超额收益"},
    {"美股原始表名": "monthlyLiquidity", "A股建议对标表": "A股月度流动性表 (Liquidity_Monthly)", "A股相关数据源表": "基于A股日度成交额、收盘价聚合计算", "核心用途": "常代入Amihud指标等流动性因子"},
    {"美股原始表名": "CompustatAnnual", "A股建议对标表": "A股三大表-年度报告表 (Financial_Annual)", "A股相关数据源表": "Wind_AShareIncome / BalanceSheet", "核心用途": "涵盖了所有年末财务快照数据（总资产、总负债、净资产等）"},
    {"美股原始表名": "m_aCompustat", "A股建议对标表": "A股三大表-TTM/滚动填充版表 (Financial_TTM)", "A股相关数据源表": "财报数据转TTM后并按月度展开对齐表", "核心用途": "在A股通常代表通过预处理将最新年报扩展铺写到每个月的记录上"},
    {"美股原始表名": "m_QCompustat", "A股建议对标表": "A股三大表-季度报告表 (Financial_Quarter)", "A股相关数据源表": "一季报/中报/三季报/年报及PIT", "核心用途": "因A股对季报披露非常规范，大量季度变化因子依赖此表"},
    {"美股原始表名": "a_aCompustat", "A股建议对标表": "同 CompustatAnnual", "A股相关数据源表": "同上", "核心用途": "美股细分年度版变体，A股可直接合表"},
    {"美股原始表名": "CRSPdistributions", "A股建议对标表": "A股分红送配表 (Dividend_Splits)", "A股相关数据源表": "Wind_AShareDividend / Tushare_dividend", "核心用途": "包含派息、分红、送股和转增信息"},
    {"美股原始表名": "m_CRSPAcquisitions", "A股建议对标表": "A股并购重组与股本变动表 (Capital_Changes)", "A股相关数据源表": "重大资产重组事件/股本变更明细", "核心用途": "跟踪企业股权变更，退市或并购事项"},
    {"美股原始表名": "CompustatPensions", "A股建议对标表": "长期待摊/应付职工薪酬表 (无需专门表)", "A股相关数据源表": "资产负债表中长期应付附注", "核心用途": "美股养老资产特殊表，A股一般通过负债表内长期待摊或职工薪酬科目搞定"},
    {"美股原始表名": "CCMLinkingTable", "A股建议对标表": "无需连接表 (合并主键 ts_code 即可)", "A股相关数据源表": "无需专门表", "核心用途": "美股历史遗留，用于将CRSP行情和财务匹配。A股行情交易与财报全以股票代码(如000001.SZ)对接"},
    {"美股原始表名": "SignalMasterTable", "A股建议对标表": "整合后统一因子宽表 (Factor_Master)", "A股相关数据源表": "在执行前根据日历行情底表预关联处理即可", "核心用途": "在准备因子计算时临时拼凑的包含所有股票各期行情的基表"},
]

df_tables = pd.DataFrame(table_mappings)
out_table_path = os.path.join(output_dir, "AShare_Table_Delivery.csv")
df_tables.to_csv(out_table_path, index=False, encoding='utf-8-sig')

# 输出Excel综合版本给客户
out_excel_path = os.path.join(output_dir, "A股化_CSAP因子映射手册.xlsx")
with pd.ExcelWriter(out_excel_path, engine='openpyxl') as writer:
    df_tables.to_excel(writer, sheet_name='数据表映射_A股', index=False)
    df_params.to_excel(writer, sheet_name='参数字段映射_A股', index=False)

print(f"Mapping complete. Created:\n1. {out_param_path}\n2. {out_table_path}\n3. {out_excel_path}")
