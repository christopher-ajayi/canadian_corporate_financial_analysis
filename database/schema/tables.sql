

CREATE SCHEMA analytics AUTHORIZATION postgres;

-- analytics.dim_company;

CREATE TABLE analytics.dim_company (
	company_id serial4 NOT NULL,
	ticker varchar(10) NOT NULL,
	company_name varchar(150) NOT NULL,
	sector varchar(100) NULL,
	industry varchar(100) NULL,
	country varchar(50) DEFAULT 'Canada'::character varying NULL,
	exchange varchar(20) NULL,
	cik varchar(20) NULL,
	CONSTRAINT dim_company_company_id_not_null NOT NULL company_id,
	CONSTRAINT dim_company_company_name_not_null NOT NULL company_name,
	CONSTRAINT dim_company_pkey PRIMARY KEY (company_id),
	CONSTRAINT dim_company_ticker_key UNIQUE (ticker),
	CONSTRAINT dim_company_ticker_not_null NOT NULL ticker
);

-----------------------------------------------------------------------------------------------------------------------------------------------------------

---- analytics.dim_date
CREATE TABLE analytics.dim_date (
	date_id serial4 NOT NULL,
	fiscal_year int4 NOT NULL,
	fiscal_period varchar(20) NULL,
	CONSTRAINT dim_date_date_id_not_null NOT NULL date_id,
	CONSTRAINT dim_date_fiscal_year_not_null NOT NULL fiscal_year,
	CONSTRAINT dim_date_pkey PRIMARY KEY (date_id)
);

-----------------------------------------------------------------------------------------------------------------------------------------------------------

--- analytics.fact_balance_sheet

CREATE TABLE analytics.fact_balance_sheet (
	balance_id serial4 NOT NULL,
	company_id int4 NULL,
	date_id int4 NULL,
	total_assets numeric NULL,
	total_liabilities numeric NULL,
	shareholders_equity numeric NULL,
	cash numeric NULL,
	total_debt numeric NULL,
	currency varchar(10) NULL,
	CONSTRAINT fact_balance_sheet_balance_id_not_null NOT NULL balance_id,
	CONSTRAINT fact_balance_sheet_pkey PRIMARY KEY (balance_id),
	CONSTRAINT uq_balance_sheet UNIQUE (company_id, date_id)
);


-- analytics.fact_balance_sheet foreign keys

ALTER TABLE analytics.fact_balance_sheet ADD CONSTRAINT fact_balance_sheet_company_id_fkey FOREIGN KEY (company_id) REFERENCES analytics.dim_company(company_id);
ALTER TABLE analytics.fact_balance_sheet ADD CONSTRAINT fact_balance_sheet_date_id_fkey FOREIGN KEY (date_id) REFERENCES analytics.dim_date(date_id);

-----------------------------------------------------------------------------------------------------------------------------------------------

--- analytics.fact_cash_flow

CREATE TABLE analytics.fact_cash_flow (
	cashflow_id serial4 NOT NULL,
	company_id int4 NULL,
	date_id int4 NULL,
	operating_cash_flow numeric NULL,
	investing_cash_flow numeric NULL,
	financing_cash_flow numeric NULL,
	free_cash_flow numeric NULL,
	currency varchar(10) NULL,
	CONSTRAINT fact_cash_flow_cashflow_id_not_null NOT NULL cashflow_id,
	CONSTRAINT fact_cash_flow_pkey PRIMARY KEY (cashflow_id),
	CONSTRAINT uq_cash_flow UNIQUE (company_id, date_id)
);


-- analytics.fact_cash_flow foreign keys

ALTER TABLE analytics.fact_cash_flow ADD CONSTRAINT fact_cash_flow_company_id_fkey FOREIGN KEY (company_id) REFERENCES analytics.dim_company(company_id);
ALTER TABLE analytics.fact_cash_flow ADD CONSTRAINT fact_cash_flow_date_id_fkey FOREIGN KEY (date_id) REFERENCES analytics.dim_date(date_id);

----------------------------------------------------------

---- analytics.fact_income_statement

CREATE TABLE analytics.fact_income_statement (
	financial_id serial4 NOT NULL,
	company_id int4 NULL,
	date_id int4 NULL,
	revenue numeric NULL,
	gross_profit numeric NULL,
	operating_income numeric NULL,
	net_income numeric NULL,
	currency varchar(10) DEFAULT 'CAD'::character varying NULL,
	CONSTRAINT fact_income_statement_financial_id_not_null NOT NULL financial_id,
	CONSTRAINT fact_income_statement_pkey PRIMARY KEY (financial_id),
	CONSTRAINT uq_income_statement UNIQUE (company_id, date_id)
);


-- analytics.fact_income_statement foreign keys

ALTER TABLE analytics.fact_income_statement ADD CONSTRAINT fact_income_statement_company_id_fkey FOREIGN KEY (company_id) REFERENCES analytics.dim_company(company_id);
ALTER TABLE analytics.fact_income_statement ADD CONSTRAINT fact_income_statement_date_id_fkey FOREIGN KEY (date_id) REFERENCES analytics.dim_date(date_id);