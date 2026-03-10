import dolphindb as ddb

s = ddb.session()
s.connect('192.168.100.43', 7731, 'admin', '123456')

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
