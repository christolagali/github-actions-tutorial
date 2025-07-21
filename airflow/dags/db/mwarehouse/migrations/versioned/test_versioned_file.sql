{% set schema_name_business_vault = "test_schema" %}

SELECT
    val,
    val2
FROM {{ schema_name_business_vault }}.test
;