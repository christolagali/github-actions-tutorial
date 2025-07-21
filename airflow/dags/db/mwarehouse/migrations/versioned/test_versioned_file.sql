{% set schema_name_business_vault = "test_schema" %}

select
val,
    val2
FROM {{ schema_name_business_vault }}.test
where
    prefix = "{{ sfdc_entity_prefix_lead }}";
;