from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker as sm



def get_table_names(without_docker = False):
    
    if without_docker:
        #create database engine without docker url
        database_url = f'postgresql://didex:didex@localhost:5432/didex'
        engine = create_engine(database_url)
        
    else:
        #create database engine with docker url
        database_url = f'postgresql://didex:didex@postgis:5432/didex'
        engine = create_engine(database_url) 
    
    
    # Get the inspector
    inspector = inspect(engine)

    return inspector.get_table_names()


def get_datahub_table_metadata(without_docker = False):
    
    if without_docker:
        database_url = f'postgresql://didex:didex@localhost:5432/didex'
        engine = create_engine(database_url)
        Session = sm(bind=engine)
    else:
        database_url = f'postgresql://didex:didex@postgis:5432/didex'
        engine = create_engine(database_url) 
        Session = sm(bind=engine) 
     
    session = Session()
    
    
    query = text("""
            WITH cats AS (
                    SELECT id, name, key FROM public.datalayers_category
                    ),
            related_tables AS (
                SELECT 
                    from_datalayer_id, 
                    STRING_AGG(d.key, ', ') AS related_tables
                FROM 
                    public.datalayers_datalayer_related_to rel
	            JOIN 
                    public.datalayers_datalayer d ON rel.to_datalayer_id = d.id
                GROUP BY 
                    from_datalayer_id
            )
            SELECT 
                dl.id,
                dl.key,
                dl.name,
                c.name AS category_name,
                c.key AS category_key,
                COALESCE(rt.related_tables, '') AS related_tables, 
                dl.description,
                dl.database_unit,
                dl.temporal_coverage,
                dl.temporal_details,
                dl.spatial_coverage,
                dl.spatial_details,
                dl.license
            FROM 
                public.datalayers_datalayer dl
            JOIN 
                cats c ON dl.category_id = c.id
            LEFT JOIN 
                related_tables rt ON dl.id = rt.from_datalayer_id
            ORDER BY 
                dl.id""".replace("\n","")
    )
    
    
    data = []
    for row in session.execute(query):
        data.append(row)
    
    final_data = []
    
    columns_to_keep = ["id", "key", "name", "category_name","category_key", "related_to", "description", "database_unit", "temporal_coverage", "temporal_details", "spatial_coverage", "spatial_details", "license"]

    for row in data:
        data = {}
        for i,col in enumerate(columns_to_keep,start=0):
            data[col] = row[i]
        
        final_data.append(data)
    
    return final_data
