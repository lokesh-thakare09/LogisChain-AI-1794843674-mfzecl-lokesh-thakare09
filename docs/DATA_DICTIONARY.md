# Data dictionary (synthetic demo)

## suppliers.csv
`supplier_id` synthetic key; `country`, `sector` categorical descriptors; `current_ratio`, `debt_to_equity`, `otif_rate`, `lead_time_days`, `lead_time_std`, `port_congestion`, `freight_cost_ratio`, `inventory_turnover`, `supplier_hhi`, `customer_hhi`, `revenue_growth`, `ebitda_margin` synthetic features; `default_12m` synthetic binary target.

## shipments.csv
`shipment_id`, `supplier_id` synthetic identifiers; `distance_km`, `cargo_value_usd`, `route_congestion`, `weather_severity`, `documentation_errors`, `carrier_reliability`, `delay_days` synthetic operational attributes; `delay` synthetic binary target.

## daily_timeseries.csv
`date`; `port_throughput_teu`; `freight_index`. Both measures are generated, not observed market data.

## Feature governance template for real sources
For every added feature document: name, formula, source, owner, unit, update frequency, expected range, point-in-time availability, missingness, transformation, financial rationale, quality checks, permitted use and licence.
