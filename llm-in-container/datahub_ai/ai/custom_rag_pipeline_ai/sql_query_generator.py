from llama_index.core import PromptTemplate
from llama_index.llms.ollama import Ollama

from datahub_ai.ai.custom_rag_pipeline_ai.utils import extract_value_from_response_string

def generate_sql_query(question_string, relavent_table_info, sql_query_generation_llm: Ollama):

    TEXT_TO_SQL_TMPL = (
        "Given an input question, first create a syntactically correct Postgres SQL statement \n\n"

        #"query to run, then look at the results of the query and return the answer. "
        #"You can order the results by a relevant column to return the most "
        #"interesting examples in the database.\n\n"
        "Never query for all the columns from a specific table, only ask for a few relevant columns given the question.\n\n"

        "Pay attention to use only the column names that you can see in the schema description. \n"
        
        "Be careful to not query for columns that do not exist. \n"

        "Pay attention to which column is in which table. \n"
        "Also, qualify column names with the table name when needed. \n"
        "'id' is not short for 'index'  \n"
        # "When asked for a shape/shapes, make the sql query return the name of the shape/shapes "

        #"When you want to filter for Countries or Regions or Districts, use shapes_shape and shapes_type and join them on shape_id=id. "
        #"Countries and Regions and Districts are writen in upercase when used in the query. "
        #"Do not use name = 'District' in this table or similar!! "
        "All the data is refering to Ghana, so do not use 'Ghana' in the query.  \n"
        #"Do NOT use aliases (like AS)."

        "In 'Table Info' cou can find the name of the tables, the description of the tables and the corresponding columns (name and data-type). The table info is formated in JSON. \n"

        "Only use tables listed below.\n"
        "Be careful to use the exact table names! Do not change them! .\n"
        "Do not provide the sql query like this: ```sql query```, instead use the given format. \n"

        "Here is the data you need: \n"
        "Question: {question_string}\n"
        "Table Info: {relavent_table_info}\n"
        # """Table Relations: table_name	foreign_key	contraint_def
        # app_user_groups	app_user_groups_group_id_e774d92c_fk_auth_group_id	FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED
        # app_user_groups	app_user_groups_user_id_e6f878f6_fk_app_user_id	FOREIGN KEY (user_id) REFERENCES app_user(id) DEFERRABLE INITIALLY DEFERRED
        # app_user_user_permissions	app_user_user_permis_permission_id_4ef8e133_fk_auth_perm	FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED
        # app_user_user_permissions	app_user_user_permissions_user_id_24780b52_fk_app_user_id	FOREIGN KEY (user_id) REFERENCES app_user(id) DEFERRABLE INITIALLY DEFERRED
        # auth_group_permissions	auth_group_permissio_permission_id_84c5c92e_fk_auth_perm	FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED
        # auth_group_permissions	auth_group_permissions_group_id_b120cbf9_fk_auth_group_id	FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED
        # auth_permission	auth_permission_content_type_id_2f476e4b_fk_django_co	FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED
        # datalayers_datalayer	datalayers_datalayer_category_id_81fb48d0_fk_datalayer	FOREIGN KEY (category_id) REFERENCES datalayers_category(id) DEFERRABLE INITIALLY DEFERRED
        # datalayers_datalayerlogentry	datalayers_datalayer_datalayer_id_248295fa_fk_datalayer	FOREIGN KEY (datalayer_id) REFERENCES datalayers_datalayer(id) DEFERRABLE INITIALLY DEFERRED
        # datalayers_datalayer_related_to	datalayers_datalayer_from_datalayer_id_3156cf01_fk_datalayer	FOREIGN KEY (from_datalayer_id) REFERENCES datalayers_datalayer(id) DEFERRABLE INITIALLY DEFERRED
        # datalayers_datalayer_related_to	datalayers_datalayer_to_datalayer_id_ee7d41f6_fk_datalayer	FOREIGN KEY (to_datalayer_id) REFERENCES datalayers_datalayer(id) DEFERRABLE INITIALLY DEFERRED
        # datalayers_datalayersource	datalayers_datalayer_datalayer_id_6698a321_fk_datalayer	FOREIGN KEY (datalayer_id) REFERENCES datalayers_datalayer(id) DEFERRABLE INITIALLY DEFERRED
        # django_admin_log	django_admin_log_content_type_id_c4bce8eb_fk_django_co	FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED
        # django_admin_log	django_admin_log_user_id_c564eba6_fk_app_user_id	FOREIGN KEY (user_id) REFERENCES app_user(id) DEFERRABLE INITIALLY DEFERRED
        # shapes_shape	shapes_shape_parent_id_105bde46_fk_shapes_shape_id	FOREIGN KEY (parent_id) REFERENCES shapes_shape(id) DEFERRABLE INITIALLY DEFERRED
        # shapes_shape	shapes_shape_type_id_cfd28982_fk_shapes_type_id	FOREIGN KEY (type_id) REFERENCES shapes_type(id) DEFERRABLE INITIALLY DEFERRED
        # taggit_taggeditem	taggit_taggeditem_content_type_id_9957a03c_fk_django_co	FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED
        # taggit_taggeditem	taggit_taggeditem_tag_id_f4f5b767_fk_taggit_tag_id	FOREIGN KEY (tag_id) REFERENCES taggit_tag(id) DEFERRABLE INITIALLY DEFERRED
        # """
        "\n\n"

        "Important!!!: Format your response exactly as stated below, taking one line: \n"
        "SQL_Query: SQL Query here \n\n"
    )
    
    TEXT_TO_SQL_PROMPT = PromptTemplate(TEXT_TO_SQL_TMPL)
    text_to_sql_prompt_string = TEXT_TO_SQL_PROMPT.format(question_string=question_string, relavent_table_info=relavent_table_info)

    #print(text_to_sql_prompt_string)

    output = sql_query_generation_llm.complete(text_to_sql_prompt_string)

    print(output)

    # extract values from response
    sql_query = extract_value_from_response_string(output.text, 'SQL_Query')



    return {
        'sql_query': sql_query,
    }