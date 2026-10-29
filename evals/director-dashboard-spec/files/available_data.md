# Available data — Brazil Consumer Health commercial team

| Source | Content | Grain | Refresh | Latency | Notes |
|---|---|---|---|---|---|
| ERP (SAP) | Sell-in: gross sales, discounts, net sales, units | SKU x customer x day | Daily | D+1 | Customers = chains, distributors, independents served directly |
| IQVIA | Sell-out: value and units at pharmacy level | SKU x channel x region x month | Monthly | ~4 weeks after month end | Covers ~82% of the pharmacy universe; independents projected |
| CRM (Salesforce) | Visits, coverage (positivação = outlets with >= 1 purchase in period), call plan compliance | Rep x outlet x visit | Daily | D+1 | Outlet master has ~18% duplicates under cleanup |
| Retail audit (vendor) | Out-of-stock (ruptura) on shelf | SKU x store, sample of 400 stores | Biweekly | 1 week | Sample skewed to large chains in Southeast |
| Price scan (vendor) | Shelf price vs. competitors | SKU x store sample | Weekly | 1 week | 120 SKUs monitored |
| Finance (BPC) | Trade spend / promotional budget, contribution margin | Brand x channel x month | Monthly | Close + 6 working days | Budget and forecast available |

Targets exist for net sales, coverage (75%) and trade spend (cap 8.5% of gross sales). No formal target for OOS; the team uses 5% informally.
