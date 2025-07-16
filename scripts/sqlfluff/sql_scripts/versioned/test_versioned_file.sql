{% set schema_name_business_vault = "test_schema" %}

SELECT
val,
val2
from {{ schema_name_business_vault }}.test
;