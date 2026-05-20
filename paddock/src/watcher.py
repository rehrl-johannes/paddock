import docker
import os
import platform

def get_architecture():
    arch = platform.machine()
    if arch == 'aarch64':
        return 'arm64'
    elif arch == 'x86_64':
        return 'x64'
    elif arch == 'armv7l':
        return 'arm'
    elif arch.startswith('arm'):
        raise RuntimeError(f'Unsupported ARM version: {arch}')
    else:
        raise RuntimeError(f'Unsupported architecture: {arch}')

IMAGE = 'docker.io/johannesrehrl/github-runners'
arch_tag = get_architecture()
IMAGE_WITH_TAG = f'{IMAGE}:{arch_tag}'

docker_client = docker.from_env()
github_pat = os.environ.get('GITHUB_PAT')

if not github_pat:
    raise RuntimeError('GITHUB_PAT is not set')

def recreate_container(container_name, repo_full_name):
    try:
        container = docker_client.containers.get(container_name)
        container.remove()
    except Exception as e:
        print(f"Could not remove container {container_name}: {e}")
    
    print(f"Creating fresh container: {container_name}")
    docker_client.containers.run(
        image=IMAGE_WITH_TAG,
        environment={
            'REPO_NAME': repo_full_name,
            'GITHUB_PAT': github_pat,
            'RUNNER_NAME': container_name,
        },
        labels={"repo_full_name": repo_full_name},
        name=container_name,
        detach=True
    )

print("Watching for stopped containers...")
for event in docker_client.events(decode=True):
    if event.get('Type') == 'container' and event.get('Action') == 'die':
        container_name = event['Actor']['Attributes'].get('name')
        repo_full_name = event['Actor']['Attributes'].get('repo_full_name')
        
        if not repo_full_name:
            print(f"Container {container_name} stopped but has no repo_full_name label, skipping...")
            continue
            
        print(f"Container {container_name} stopped, recreating fresh container...")
        recreate_container(container_name, repo_full_name)