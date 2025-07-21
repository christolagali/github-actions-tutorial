SELECT * 
from ${schema_name_data_mart}.test
where
    prefix = "{{ sfdc_entity_prefix_lead }}";