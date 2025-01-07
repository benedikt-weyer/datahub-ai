from sqlalchemy import create_engine, inspect


def get_table_names(without_docker = False):
    #create database engine
    database_url = f'postgresql://didex:didex@{"localhost" if without_docker else "postgis"}:5432/didex'
    engine = create_engine(database_url)

    # Get the inspector
    inspector = inspect(engine)

    return inspector.get_table_names()


print(get_table_names(True))