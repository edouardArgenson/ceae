# https://towardsdatascience.com/reading-and-writing-files-from-to-amazon-s3-with-pandas-ccaf90bfe86c


import io

import boto3
import pandas as pd


def dump_append(
    df: pd.DataFrame,
    bucket_name: str,
    path: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
) -> None:
    # Initiate boto s3 client.
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    # Fetch.
    inplace_df = fetch(s3_client=s3_client, bucket_name=bucket_name, path=path)

    # Append.
    merged_df = pd.concat([inplace_df, df])

    # Dump.
    dump(s3_client=s3_client, df=merged_df, bucket_name=bucket_name, path=path)


def fetch(s3_client, bucket_name: str, path: str) -> pd.DataFrame:
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=path)
    except s3_client.exceptions.NoSuchKey:
        return pd.DataFrame()

    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status != 200:
        raise ValueError(f"Unsuccessful S3 get_object response. Status - {status}")

    print(f"Successful S3 get_object response. Status - {status}")
    return pd.read_csv(response.get("Body"))
    
    
def dump(s3_client, df: pd.DataFrame, bucket_name: str, path: str) -> None:
    with io.StringIO() as csv_buffer:
        df.to_csv(csv_buffer, index=False)

        response = s3_client.put_object(
            Bucket=bucket_name,
            Key=path,
            Body=csv_buffer.getvalue(),
        )

        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

        if status != 200:
            raise ValueError("Unsuccessful S3 put_object response. Status - {status}")
        print(f"Successful S3 put_object response. Status - {status}")
