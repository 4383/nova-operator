from oslo_config import cfg
import yaml
import os

config_file_path = "/etc/nova/nova.conf"

CONF = cfg.CONF
CONF(default_config_files=[config_file_path])

# Convert config into yaml
config_data = {}
for section in CONF.sections():
    config_data[section] = dict(CONF.items(section))
config_yaml = yaml.dump(config_data, default_flow_style=False)

# Create a kubernetes config map with the yaml generated previously
configmap_name = "nova-config"
namespace = "openstack"
configmap_data = {
    "nova-config.yaml": config_yaml
}
kubectl_cmd = f"kubectl create configmap {configmap_name} --namespace {namespace} --from-literal=config.yaml='{config_yaml}'"
os.system(kubectl_cmd)
