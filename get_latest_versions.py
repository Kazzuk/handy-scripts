from xml.etree import ElementTree
import requests

BASE_URL = "https://repo.opencollab.dev/maven-snapshots"
GROUP_ID = "org.cloudburstmc.protocol"
ARTIFACT_IDS = ["bedrock-codec", "bedrock-connection", "common"]
VERSION = "3.0.0.Beta1-SNAPSHOT"


def construct_metadata_url(artifact_id: str) -> str:
    return f"{BASE_URL}/{GROUP_ID.replace('.', '/')}/{artifact_id}/{VERSION}/maven-metadata.xml"


def format_version(artifact_id: str, timestamp: str, build_number: str) -> str:
    return f"{artifact_id}-{VERSION.replace('-SNAPSHOT', '')}-{timestamp}-{build_number}"


def get_latest_version(session: requests.Session, artifact_id: str) -> str | None:
    metadata_url = construct_metadata_url(artifact_id)
    try:
        response = session.get(metadata_url)
        response.raise_for_status()
        root = ElementTree.fromstring(response.content)
        timestamp = root.find(".//timestamp").text
        build_number = root.find(".//buildNumber").text
        return format_version(artifact_id, timestamp, build_number)
    except (ElementTree.ParseError, requests.HTTPError, AttributeError) as error:
        print(error)
        return None


def main():
    with requests.Session() as session:
        for artifact_id in ARTIFACT_IDS:
            latest_version = get_latest_version(session, artifact_id)
            if latest_version is not None:
                print(latest_version)
            else:
                print(f"Failed to fetch latest version for {artifact_id}")


if __name__ == "__main__":
    main()
