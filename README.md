# Paddock

Paddock is a lightweight tool for automating the management of containerised GitHub Actions runners.

## How to install

### Debian

Add the Paddock repository and install:

```bash
curl -1sLf 'https://dl.cloudsmith.io/public/paddock/paddock/setup.deb.sh' | sudo -E bash
sudo apt install paddock
```

During install you will be prompted regarding your Github Personal Access Token and which tag you want to use in order to identify repositories for which runners should be created.
