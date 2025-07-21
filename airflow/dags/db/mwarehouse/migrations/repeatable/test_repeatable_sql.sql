SELECT * 
FROM ${schema_name_data_mart}.test
WHERE
    prefix = "{{ sfdc_entity_prefix_lead }}"
;