from datahub_ai.data_access.datahub_tables_access import get_datahub_table_metadata 


def get_datahub_tables_metadata(without_docker_flag=False):
    
    datahub_data = get_datahub_table_metadata(without_docker = without_docker_flag)

    table_map = {}
    
    for table in sorted(datahub_data, key=lambda table: table["id"]):        
        
        if table["description"].find("you can find follow up") != -1:
            table["description"] =  'not available'
            
        if table['related_to'] == '':
           related= f"and it is not related to any tables. "
        else:
            related = f" and it is related to the tables {table['related_to']}."
        
        description = (
        f"This table belongs to the category '{table['category_name']}' and the category key is '{table['category_key']}'. "
        f"The contained information describes {table['name']}, {related}. "
        f"The information this table provides is {table['description']}, measured in '{table['database_unit']}'."
        )
        
        if table['temporal_coverage']:
            description += f"The temporal coverage is {table['temporal_coverage']}."
        
        if table['temporal_details']:
            description += f"The temporal resolution is {table['temporal_details']}."
        
        if table['spatial_coverage']:
            description += f"The spatial coverage is {table['spatial_coverage']}."
        
        if table['spatial_details']:
            description += f"The spacial resolution is {table['spatial_details']}."
        
        if table['license']:
            description += f"The license for this table is {table['license']}."

            
        table_map[table['key']] = description
        
    return table_map
