{% set schema_name_business_vault = "test_schema" %}

SELECT
    val,
val2
from {{datashare_name_minkhouse_eu}}.{{ schema_name_mi_studio }}.test
where
    prefix = "{{sfdc_entity_prefix_lead}}"
;