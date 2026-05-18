import os
import docker
import requests
import traceback

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
        raise RuntimeError(f'Unsupported ARM version: {arch} (minimum ARMv7 required)')
    else:
        raise RuntimeError(f'Unsupported architecture: {arch}')

IMAGE = 'docker.io/johannesrehrl/github-runners'
arch_tag = get_architecture()
IMAGE_WITH_TAG = f'{IMAGE}:{arch_tag}'

print("Scheduled check for changes...")

docker_client = docker.from_env()

github_pat = os.environ.get('GITHUB_PAT')
github_tag = os.environ.get('GITHUB_TAG')
api = 'https://api.github.com'

headers = {'Authorization': f'token {github_pat}'}

if not github_pat:
    raise RuntimeError('GITHUB_PAT is not set')
if not github_tag:
    raise RuntimeError('GITHUB_TAG is not set')

try:
    docker_client.images.pull(IMAGE, tag=arch_tag)
    docker_client.containers.prune()

    res = requests.get(api + '/user/repos', headers=headers)
    res.raise_for_status()
    response = res.json()

    # Repos which are intended for self-hosted runners must have the correct Github topic (github_tag)
    repos_to_run = {
        repo['name'] + '-runner': repo['full_name']
        for repo in response
        if github_tag in repo['topics']
    }
    running_containers = {c.name: c.id for c in docker_client.containers.list()}

    if set(repos_to_run.keys()) != set(running_containers.keys()):
        print("Repository list changed, regenerating stack...")

        # Check for repos that are missing a runner
        for repo in set(repos_to_run.keys()) - set(running_containers.keys()):
            print("Creating new runner container:", repo)

            env = {
                'REPO_NAME': repos_to_run[repo],
                'GITHUB_PAT': github_pat,
                'RUNNER_NAME': repo,
            }

            container = docker_client.containers.run(
                image=IMAGE_WITH_TAG, 
                environment=env, 
                restart_policy={"Name": "always"},
                name=repo,
                detach=True)

        # Check for runners that serve a no longer applicable repo
        for repo in set(running_containers.keys()) - set(repos_to_run.keys()):
            print("Shutting down unneeded runner container:", repo)
            container = docker_client.containers.get(running_containers[repo])
            container.stop()             
            container.remove() 

    else:
        print("Check passed, no changes to repo list.")

    running_containers = {c.name: c.id for c in docker_client.containers.list()}
    new_image_id = docker_client.images.get(IMAGE_WITH_TAG).id
    for name, container_id in running_containers.items():
        container = docker_client.containers.get(container_id)
        if container.image.id != new_image_id:
            print(f"Restarting {name} on new image...")
            container.stop()
            container.remove()

            env = {
                'REPO_NAME': repos_to_run[name],
                'GITHUB_PAT': github_pat,
                'RUNNER_NAME': name,
            }

            docker_client.containers.run(
                image=IMAGE_WITH_TAG,
                environment=env,
                restart_policy={"Name": "always"},
                name=name,
                detach=True
        )
        

except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()