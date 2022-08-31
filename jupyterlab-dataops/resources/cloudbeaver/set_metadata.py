from google.cloud import compute_v1
import requests


def get_gooogle_instance_property(attribute_name):
    try:
        response = requests.get(
            f'http://metadata.google.internal/computeMetadata/v1/instance/{attribute_name}',
            headers={'Metadata-Flavor': 'Google'})
        if response.status_code == 200:
            return response.text
        return None
    except:
        return None


def get_google_project_attribute(attribute_name):
    try:
        response = requests.get(
            f"http://metadata/computeMetadata/v1/project/{attribute_name}",
            headers={'Metadata-Flavor': 'Google'})
        if response.status_code == 200:
            return response.text
        return None
    except:
        return None


try:
    instance = get_gooogle_instance_property('hostname').split('.')[0]
    zone = get_gooogle_instance_property('zone').split('/')[-1]
    project = get_google_project_attribute('project-id')

    instance_client = compute_v1.InstancesClient()
    existing_meta = instance_client.get(
        project=project, zone=zone, instance=instance).metadata
    entries = {el.key: el.value for el in existing_meta.items}

    entries['custom-proxy-agent'] = 'gcr.io/getindata-images-public/inverting-proxy'

    instance_client.set_metadata(project=project, zone=zone, instance=instance, metadata_resource={
                                 "items": [{"key": k, "value": v} for k, v in entries.items()], "fingerprint": existing_meta.fingerprint})
except:
    pass