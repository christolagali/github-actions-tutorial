{% set schema_name_business_vault = "test_schema" %}

select
    val,
val2
from {{ schema_name_business_vault }}.test
;