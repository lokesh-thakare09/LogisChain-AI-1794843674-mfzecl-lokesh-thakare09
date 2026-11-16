"""Ten parametrised disruption scenarios with multi-channel financial impacts."""
SCENARIOS = [
 {"name":"Suez Canal blockage","severity":5,"duration_days":12,"freight_pct":.65,"delay_days":10,"inventory_days":8,"lc_expiry":.18,"insurance_claim":.12},
 {"name":"Major port congestion","severity":4,"duration_days":9,"freight_pct":.25,"delay_days":7,"inventory_days":5,"lc_expiry":.12,"insurance_claim":.05},
 {"name":"Carrier bankruptcy","severity":5,"duration_days":18,"freight_pct":.35,"delay_days":14,"inventory_days":6,"lc_expiry":.22,"insurance_claim":.18},
 {"name":"Extreme weather event","severity":4,"duration_days":6,"freight_pct":.18,"delay_days":6,"inventory_days":4,"lc_expiry":.08,"insurance_claim":.25},
 {"name":"Supplier insolvency","severity":5,"duration_days":25,"freight_pct":.12,"delay_days":16,"inventory_days":12,"lc_expiry":.20,"insurance_claim":.04},
 {"name":"Demand surge","severity":3,"duration_days":21,"freight_pct":.20,"delay_days":3,"inventory_days":10,"lc_expiry":.04,"insurance_claim":.01},
 {"name":"Demand collapse","severity":3,"duration_days":30,"freight_pct":-.12,"delay_days":0,"inventory_days":18,"lc_expiry":.03,"insurance_claim":.01},
 {"name":"Trade restriction","severity":4,"duration_days":30,"freight_pct":.30,"delay_days":12,"inventory_days":9,"lc_expiry":.16,"insurance_claim":.08},
 {"name":"Cyberattack on port systems","severity":4,"duration_days":5,"freight_pct":.22,"delay_days":8,"inventory_days":5,"lc_expiry":.14,"insurance_claim":.03},
 {"name":"Cold-chain failure","severity":4,"duration_days":3,"freight_pct":.08,"delay_days":3,"inventory_days":2,"lc_expiry":.07,"insurance_claim":.35},
]
