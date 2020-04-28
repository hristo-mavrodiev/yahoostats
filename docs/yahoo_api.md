Hosts:

    query1.finance.yahoo.com HTTP/1.0
    query2.finance.yahoo.com HTTP/1.1 difference between HTTP/1.0 & HTTP/1.1

If you plan to use a proxy or persistent connections use query2.finance.yahoo.com
But for the purposes of this post the host used for the example URLs is not meant to imply
anything about the path it's being used with.

    We will use HTTP/1.1

Fundamental Data

    /v10/finance/quoteSummary/AAPL?modules= (Full list of modules below)

(substitute your symbol for: AAPL)
Inputs for the ?modules= query:

    modules = [
     'assetProfile',
     'incomeStatementHistory',
     'incomeStatementHistoryQuarterly',
     'balanceSheetHistory',
     'balanceSheetHistoryQuarterly',
     'cashflowStatementHistory',
     'cashflowStatementHistoryQuarterly',
     'defaultKeyStatistics',
     'financialData',
     'calendarEvents',
     'secFilings',
     'recommendationTrend',
     'upgradeDowngradeHistory',
     'institutionOwnership',
     'fundOwnership',
     'majorDirectHolders',
     'majorHoldersBreakdown',
     'insiderTransactions',
     'insiderHolders',
     'netSharePurchaseActivity',
     'earnings',
     'earningsHistory',
     'earningsTrend',
     'industryTrend',
     'indexTrend',
     'sectorTrend' ] #### Example URL:


Querying for: assetProfile and earningsHistory

The %2C is the Hex representation of , and needs to be inserted between each module you
request. details about the hex encoding bit (if you care)
Credits : https://github.com/Gunjan933/stock-market-scraper/blob/master/stock-market-scraper.ipynb

