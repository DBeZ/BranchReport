###########################################################################
# Query for getting all roles for all non next-generation users in system
###########################################################################
import pandas as pd
from connect_to_database import connect_to_database
from user_specific_extractor import login_sql


# SQL query to receive all user roles for each user
def users_with_all_roles_query(connection):

    fields_final_display = "user_ID, shortname AS role, roleid as roleID, assignRoleDate "

    fields_role_assignments_to_users="userid as user_ID , roleid , FROM_UNIXTIME(timemodified, '%Y-%m-%d') AS assignRoleDate "
    table_role_assignments = "shecodes_shecodes.mdl_role_assignments "

    table_roles = "shecodes_shecodes.mdl_role "
    on_role="userRoleSubset.roleid=mdl_role.id "

    condition_user_id_not_null="user_ID IS NOT NULL"
    #TODO remove admin_ng and boyer on sql level using where
    query = (
        f"SELECT {fields_final_display} "

        f"FROM (SELECT {fields_role_assignments_to_users} "
        f"FROM {table_role_assignments} "
        f") AS userRoleSubset "

        f"RIGHT JOIN {table_roles} "
        f"ON {on_role} "
        f"WHERE {condition_user_id_not_null} "
    )
    cursor = connection.cursor()
    cursor.execute(query)
    columns = cursor.column_names
    query_res_df = pd.DataFrame(cursor.fetchall())
    query_res_df.columns = list(columns)

    connection.close()
    cursor.close()

    fields_dict = {  # IMPORTANT: IF THIS IS UPDATED ALSO UPDATE SQL QUERY AND TYPE DICTIONARY BELOW
        "user": "user_ID",  # user connect ID
        "role_name": "role",  # Role name
        "role_id": "roleID",  # Role ID
        "role_assign": "assignRoleDate",  # Date role was assigned
    }

    field_data_types_dict = {
        "user": "int",  # user connect ID
        "role_name": "string",  # Role name
        "role_id": "int",  # Role ID
        "role_assign": "datetime",  # Date role was assigned
    }
    return query_res_df, fields_dict, field_data_types_dict


## Login to database and query to recive all activity enteries in a given date range
def retrieve_users_with_roles(sql_details_file_name, user_specific_dir):
    sql_login_dict = login_sql(sql_details_file_name, user_specific_dir)
    connection = connect_to_database(sql_login_dict["User"], sql_login_dict["Pass"], sql_login_dict["Database"], sql_login_dict["Host"], sql_login_dict["Port"])
    print("User role data being retrieved")
    data_df, fields_dict, field_data_types_dict=users_with_all_roles_query(connection)
    print("Data retrieval done!")
    return data_df,fields_dict, field_data_types_dict

