from google.cloud import compute_v1
import requests
import jinja2
import os

TEMPLATE_PATH = os.getenv("TEMPLATE_PATH", "/opt/cloudbeaver/conf/initial-data-sources.conf.j2")
SOURCES_PATH = os.getenv("SOURCES_PATH", "/opt/cloudbeaver/conf/initial-data-sources.conf")

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

def render_template(project_id):
    loader = jinja2.FileSystemLoader(searchpath=os.path.dirname(TEMPLATE_PATH))
    env = jinja2.Environment(loader=loader)
    try:
        template = env.get_template(os.path.basename(TEMPLATE_PATH))
    except jinja2.exceptions.TemplateNotFound:
        return None
    return template.render({'project_id': project_id})

def configure_bigquery_connection(project_id):
    rendered = render_template(project_id)
    with open(SOURCES_PATH, 'w') as f:
        f.write(rendered)
    
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
    
    configure_bigquery_connection(project)
except:
    pass