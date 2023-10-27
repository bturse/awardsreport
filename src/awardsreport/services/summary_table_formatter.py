from awardsreport.schemas import summary_tables_schemas
from sqlalchemy import Result
from typing import TypedDict, List


class SchemaFieldT(TypedDict):
    name: str | None
    title: str | None
    type: str | None


class SchemaFieldDictT(TypedDict):
    fields: list[SchemaFieldT]


def create_schema_field_dict(
    gb_schema: summary_tables_schemas.GroupByStatementSchema,
) -> SchemaFieldDictT:
    """Create fields dict for TableSchema.

    params:
        gb_schema: summary_tables_schemas.GroupByStatementSchema

    returns SchemaFieldDictT
    """
    schema_field_list: List[SchemaFieldT] = []
    for key in gb_schema.gb:
        schema_field: SchemaFieldT = {"name": key, "title": None, "type": None}
        field = summary_tables_schemas.TableSchemaData.__fields__.get(key)
        if field:
            schema_field["title"] = field.field_info.title
            schema_field["type"] = field.field_info.extra.get("response_type")
        schema_field_list.append(schema_field)
    schema_field_list.append(
        {"name": "obligations", "title": "obligations", "type": "number"}
    )
    schema_field_dict = SchemaFieldDictT(fields=schema_field_list)
    return schema_field_dict


def create_data_schema_list(
    group_by_schema: summary_tables_schemas.GroupByStatementSchema, results: Result
) -> list[dict]:
    """Convert SQLAlchemy query results to dict suitable for pandas.read_json with orient='table'

    args:
        group_by_schema: summary_tables_schemas.GroupByStatementSchema
        results: Result

    return list[dict]
    """
    data_schema_list = []
    for result in results:
        r = dict(zip(group_by_schema.gb, result))
        r["obligations"] = result[-1]  # type: ignore
        data_schema_list.append(r)
    return data_schema_list


def create_table_schema_response(
    group_by_schema: summary_tables_schemas.GroupByStatementSchema, results: Result
) -> dict:
    """Format results as JSON Table Schema for summary_tables response.

    args:
        group_by_schema: summary_tables_schemas.GroupByStatementSchema
        results: Result

    return dict
    """
    data_schema_list = create_data_schema_list(group_by_schema, results)
    schema_field_dict = create_schema_field_dict(group_by_schema)
    table_schema = {"schema": schema_field_dict, "data": data_schema_list}
    table_schema_response = summary_tables_schemas.TableSchema.parse_obj(
        table_schema
    ).dict(exclude_none=True, by_alias=True)
    return table_schema_response
