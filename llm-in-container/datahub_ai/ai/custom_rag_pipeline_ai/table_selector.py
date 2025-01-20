from llama_index.core import PromptTemplate
from llama_index.llms.ollama import Ollama

from datahub_ai.ai.custom_rag_pipeline_ai.utils import extract_value_from_response_string

def select_important_tables(query_string, table_info, table_selector_llm: Ollama):

    SELECT_TABLE_TMPL = (
        "Select 0 to 4 tables that should be used in a sql query to answer the question \n"
        "Please also evaluate if an sql query is in general necessary to answer the question \n"
        "When you select at least one table then also provide a reason for selecting those tables \n"
        "Here is the data you need: \n"
        "Question: {query_string}\n"
        "Table Info: {table_info}\n"
        """Table Relations: table_name	foreign_key	contraint_def
app_user_groups	app_user_groups_group_id_e774d92c_fk_auth_group_id	FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED
app_user_groups	app_user_groups_user_id_e6f878f6_fk_app_user_id	FOREIGN KEY (user_id) REFERENCES app_user(id) DEFERRABLE INITIALLY DEFERRED
app_user_user_permissions	app_user_user_permis_permission_id_4ef8e133_fk_auth_perm	FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED
app_user_user_permissions	app_user_user_permissions_user_id_24780b52_fk_app_user_id	FOREIGN KEY (user_id) REFERENCES app_user(id) DEFERRABLE INITIALLY DEFERRED
auth_group_permissions	auth_group_permissio_permission_id_84c5c92e_fk_auth_perm	FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED
auth_group_permissions	auth_group_permissions_group_id_b120cbf9_fk_auth_group_id	FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED
auth_permission	auth_permission_content_type_id_2f476e4b_fk_django_co	FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED
datalayers_datalayer	datalayers_datalayer_category_id_81fb48d0_fk_datalayer	FOREIGN KEY (category_id) REFERENCES datalayers_category(id) DEFERRABLE INITIALLY DEFERRED
datalayers_datalayerlogentry	datalayers_datalayer_datalayer_id_248295fa_fk_datalayer	FOREIGN KEY (datalayer_id) REFERENCES datalayers_datalayer(id) DEFERRABLE INITIALLY DEFERRED
datalayers_datalayer_related_to	datalayers_datalayer_from_datalayer_id_3156cf01_fk_datalayer	FOREIGN KEY (from_datalayer_id) REFERENCES datalayers_datalayer(id) DEFERRABLE INITIALLY DEFERRED
datalayers_datalayer_related_to	datalayers_datalayer_to_datalayer_id_ee7d41f6_fk_datalayer	FOREIGN KEY (to_datalayer_id) REFERENCES datalayers_datalayer(id) DEFERRABLE INITIALLY DEFERRED
datalayers_datalayersource	datalayers_datalayer_datalayer_id_6698a321_fk_datalayer	FOREIGN KEY (datalayer_id) REFERENCES datalayers_datalayer(id) DEFERRABLE INITIALLY DEFERRED
django_admin_log	django_admin_log_content_type_id_c4bce8eb_fk_django_co	FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED
django_admin_log	django_admin_log_user_id_c564eba6_fk_app_user_id	FOREIGN KEY (user_id) REFERENCES app_user(id) DEFERRABLE INITIALLY DEFERRED
shapes_shape	shapes_shape_parent_id_105bde46_fk_shapes_shape_id	FOREIGN KEY (parent_id) REFERENCES shapes_shape(id) DEFERRABLE INITIALLY DEFERRED
shapes_shape	shapes_shape_type_id_cfd28982_fk_shapes_type_id	FOREIGN KEY (type_id) REFERENCES shapes_type(id) DEFERRABLE INITIALLY DEFERRED
taggit_taggeditem	taggit_taggeditem_content_type_id_9957a03c_fk_django_co	FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED
taggit_taggeditem	taggit_taggeditem_tag_id_f4f5b767_fk_taggit_tag_id	FOREIGN KEY (tag_id) REFERENCES taggit_tag(id) DEFERRABLE INITIALLY DEFERRED
"""
        "\n\n"
        "Format your response as stated below, each taking one line: \n"
        "Is_SQL_Query_Necessary: true or false \n"
        "Selected_Tables: table_name_1, table_name2... \n"
        "Reason_For_Selecting_Those_Tables: The reason for selecting the tables here, when necessary. Else leave empty \n"
    )
    SLECT_TABLE_PROMPT = PromptTemplate(SELECT_TABLE_TMPL)
    select_table_prompt_string = SLECT_TABLE_PROMPT.format(query_string=query_string, table_info=table_info)
    print(select_table_prompt_string)
    output = table_selector_llm.complete(select_table_prompt_string)

    print(output)

    # extract values from response
    is_sql_query_necessary = extract_value_from_response_string(output.text, 'SQL_Query_Necessary')
    print(is_sql_query_necessary)
    is_sql_query_necessary_bool = True if is_sql_query_necessary == 'true' else False
    selected_tables = extract_value_from_response_string(output.text, 'Selected_Tables')



    return {
        'is_sql_query_necessary': is_sql_query_necessary_bool,
        'relavant_tables': selected_tables
    }