import os
import boto3
import argparse


def get_content_type(file_path: str):
    extension = os.path.splitext(file_path)[-1]
    contents = {
        ".js": "application/javascript",
        ".html": "text/html",
        ".txt": "text/plain",
        ".json": "application/json",
        ".ico": "image/x-icon",
        ".svg": "image/svg+xml",
        ".css": "text/css",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".map": "binary/octet-stream",
    }

    if extension in contents:
        return contents[extension]

    return "application/octet-stream"


def main():
    """Uploads the contents of the build directory to the given s3 bucket
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--endpoint-url", help="""
    specify the S3 endpoint url to upload the files to.
    If no endpoint is specified then the default
    defined in the .aws/ directory is used.
    """
    )
    args = parser.parse_args()

    endpoint_url = args.endpoint_url

    s3 = boto3.client("s3", endpoint_url=endpoint_url)
    for root, _, files in os.walk(os.path.join("clinic_frontend", "build")):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Uploading: {os.path.join(root, file)}")
            s3.upload_file(
                file_path,
                "frontend",
                file_path.removeprefix(os.path.join("clinic_frontend", "build") + "/"),
                ExtraArgs={"ContentType": get_content_type(file)},
            )


if __name__ == "__main__":
    main()
