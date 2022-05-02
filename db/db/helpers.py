from string import Template

DB_URI_TEMPLATE = Template("$dialect://$user:$password@$host/$dbname")

def build_database_uri(
    dialect: str, user: str, password: str, host: str, dbname: str
) -> str:
    return DB_URI_TEMPLATE.substitute(
        dialect=dialect,
        user=user,
        password=password,
        host=host,
        dbname=dbname,
    )
