import os

import dolphindb as ddb


def require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise SystemExit(f"Missing required env var: {name}")
    return value


s = ddb.session()
s.connect(
    require_env("DDB_HOST"),
    int(require_env("DDB_PORT")),
    require_env("DDB_USER"),
    require_env("DDB_PASSWORD"),
)

test_script = """
try {
    use CSAPDataSimulation
    use CSAPFactors

    // Simulate data
    gvkeyList = 10970 10910
    startYear = 1987
    endYear = 2023
    result = CSAPDataSimulation::CSAPDataSimulation(gvkeyList, startYear, endYear)
    
    // We get CompustatAnnual which has `at` (Total Assets)
    // Let's create a synthetic table for testing `assetGrowth`
    t = result.CompustatAnnual
    t = select at, datadate as time_avail_m from t 
    update t set time_avail_m = datetimeParse(string(time_avail_m)+".01", "yyyy.MM.dd") // pretend monthly
    
    // Run the factor on simulated data
    t = select *, CSAPFactors::assetGrowth(time_avail_m, at) as asset_growth from t
    
    return t
} catch(ex) {
    return string(ex)
}
"""
print("Testing calculation...")
res = s.run(test_script)
print("Calculation Result:", res)
