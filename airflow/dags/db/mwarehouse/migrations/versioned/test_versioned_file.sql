{% set schema_name_business_vault = "test_schema" %}

SELECT
    val,
    val2
FROM {{ schema_name_business_vault }}.test
WHERE 
    prefix = "{{ sfdc_entity_prefix_lead }}"
;