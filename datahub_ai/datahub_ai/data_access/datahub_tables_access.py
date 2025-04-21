from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker as sm
import os

# Get database connection parameters from environment variables
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASSWORD")
db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT", "5432")
db_name = os.environ.get("DB_NAME")

database_url = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
engine = create_engine(database_url)



def get_table_names():
    # Get the inspector
    inspector = inspect(engine)

    return inspector.get_table_names()

def get_column_infos(table_name):
    # Get the inspector
    inspector = inspect(engine)

    columns = inspector.get_columns(table_name)

    column_infos = [{'column_name': column['name'], 'data_type': column['type']} for column in columns]

    return column_infos


def get_datahub_table_metadata():
    session_maker = sm(bind=engine)
    session = session_maker()

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


def execute_generated_query(sql_query):
    session_maker = sm(bind=engine)
    session = session_maker()

    # set session to read only
    session.execute(text("SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY"))

    # execute and return query
    result = session.execute(text(sql_query))
    query_results = [{column: value for column, value in row.items()} for row in result.mappings()]

    return query_results
