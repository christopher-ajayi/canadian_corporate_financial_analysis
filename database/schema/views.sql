-- analytics.v_asset_growth source

CREATE OR REPLACE VIEW analytics.v_asset_growth
AS SELECT c.company_name,
    d.fiscal_year,
    b.total_assets,
    lag(b.total_assets) OVER (PARTITION BY c.company_name ORDER BY d.fiscal_year) AS prior_assets,
    round((b.total_assets - lag(b.total_assets) OVER (PARTITION BY c.company_name ORDER BY d.fiscal_year)) 
        / NULLIF(lag(b.total_assets) OVER (PARTITION BY c.company_name ORDER BY d.fiscal_year), 0::numeric) * 100::numeric, 2) AS asset_growth_pct
   FROM analytics.fact_balance_sheet b
     JOIN analytics.dim_company c ON b.company_id = c.company_id
     JOIN analytics.dim_date d ON b.date_id = d.date_id
  WHERE b.total_assets IS NOT NULL;


-- analytics.v_cash_flow_trends source

CREATE OR REPLACE VIEW analytics.v_cash_flow_trends
AS SELECT c.company_name,
    d.fiscal_year,
    cf.operating_cash_flow,
    cf.investing_cash_flow,
    cf.financing_cash_flow,
    cf.free_cash_flow
   FROM analytics.fact_cash_flow cf
     JOIN analytics.dim_company c ON cf.company_id = c.company_id
     JOIN analytics.dim_date d ON cf.date_id = d.date_id;



-- analytics.v_company_summary source

CREATE OR REPLACE VIEW analytics.v_company_summary
AS SELECT c.company_name,
    c.sector,
    max(d.fiscal_year) AS latest_year,
    max(i.revenue) FILTER (WHERE d.fiscal_year = (( SELECT max(d2.fiscal_year) AS max
           FROM analytics.fact_income_statement i2
             JOIN analytics.dim_date d2 ON i2.date_id = d2.date_id
          WHERE i2.company_id = c.company_id))) AS latest_revenue,
    max(i.net_income) FILTER (WHERE d.fiscal_year = (( SELECT max(d2.fiscal_year) AS max
           FROM analytics.fact_income_statement i2
             JOIN analytics.dim_date d2 ON i2.date_id = d2.date_id
          WHERE i2.company_id = c.company_id))) AS latest_net_income,
    max(b.total_assets) FILTER (WHERE d.fiscal_year = (( SELECT max(d2.fiscal_year) AS max
           FROM analytics.fact_balance_sheet b2
             JOIN analytics.dim_date d2 ON b2.date_id = d2.date_id
          WHERE b2.company_id = c.company_id))) AS latest_total_assets
   FROM analytics.dim_company c
     LEFT JOIN analytics.fact_income_statement i ON c.company_id = i.company_id
     LEFT JOIN analytics.fact_balance_sheet b ON c.company_id = b.company_id
     LEFT JOIN analytics.dim_date d ON i.date_id = d.date_id
  GROUP BY c.company_name, c.sector, c.company_id;



  -- analytics.v_debt_ratios source

CREATE OR REPLACE VIEW analytics.v_debt_ratios
AS SELECT c.company_name,
    d.fiscal_year,
    b.total_assets,
    b.total_liabilities,
    b.shareholders_equity,
    b.total_debt,
    round(b.total_liabilities / NULLIF(b.total_assets, 0::numeric), 4) AS liabilities_to_assets,
    round(b.total_debt / NULLIF(b.total_assets, 0::numeric), 4) AS debt_to_assets,
    round(b.total_debt / NULLIF(b.shareholders_equity, 0::numeric), 4) AS debt_to_equity
   FROM analytics.fact_balance_sheet b
     JOIN analytics.dim_company c ON b.company_id = c.company_id
     JOIN analytics.dim_date d ON b.date_id = d.date_id
  WHERE b.total_assets IS NOT NULL;




  -- analytics.v_profitability source

CREATE OR REPLACE VIEW analytics.v_profitability
AS SELECT c.company_name,
    d.fiscal_year,
    i.revenue,
    i.gross_profit,
    i.operating_income,
    i.net_income,
    round(i.gross_profit / NULLIF(i.revenue, 0::numeric) * 100::numeric, 2) AS gross_margin_pct,
    round(i.operating_income / NULLIF(i.revenue, 0::numeric) * 100::numeric, 2) AS operating_margin_pct,
    round(i.net_income / NULLIF(i.revenue, 0::numeric) * 100::numeric, 2) AS net_margin_pct
   FROM analytics.fact_income_statement i
     JOIN analytics.dim_company c ON i.company_id = c.company_id
     JOIN analytics.dim_date d ON i.date_id = d.date_id
  WHERE i.revenue IS NOT NULL;



  -- analytics.v_revenue_growth source

CREATE OR REPLACE VIEW analytics.v_revenue_growth
AS SELECT c.company_name,
    d.fiscal_year,
    i.revenue,
    lag(i.revenue) OVER (PARTITION BY c.company_name ORDER BY d.fiscal_year) AS prior_revenue,
    round((i.revenue - lag(i.revenue) OVER (PARTITION BY c.company_name ORDER BY d.fiscal_year)) / NULLIF(lag(i.revenue) OVER (PARTITION BY c.company_name ORDER BY d.fiscal_year), 0::numeric) * 100::numeric, 2) AS revenue_growth_pct
   FROM analytics.fact_income_statement i
     JOIN analytics.dim_company c ON i.company_id = c.company_id
     JOIN analytics.dim_date d ON i.date_id = d.date_id
  WHERE i.revenue IS NOT NULL;

