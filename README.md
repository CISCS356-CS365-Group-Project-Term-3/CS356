# Setup

### 1. install Docker
Linux: https://docs.docker.com/engine/install/
Windows: https://docs.docker.com/desktop/setup/install/windows-install/
### 2. clone this repository
`cd` to wherever you want to project directories to be

clone the repository
```git clone https://github.com/CISCS356-CS365-Group-Project-Term-3/CS356.git```

enter the project root directory
```cd CS356```
### 3. Create an SSH key for JWT auth
create an SSH directory

```mkdir ssh```

Generate a 2048-bit RSA key

```ssh-keygen -t rsa -b 2048 -f ./ssh/id_rsa```

Hit enter to skip passphrase creation

If this has worked correctly, you should have an `id_rsa` file in the ssh directory starting with `-----BEGIN OPENSSH PRIVATE KEY-----` and an `id_rsa.pub` file starting with `ssh-rsa`
### 4. Add raw test video to /resources/input
_if not unzipping the provided_ `input.zip` _test video, then database and config map will need to be updated to reflect the video you have available._
### 5. Start the system
If you have make installed, you can use `make compose-engine-rebuild`

Otherwise, run the commands manually:

```docker compose --profile mongo --profile experiment-management up --build --force-recreate engine mongo experiment-management infra-management user-management web results-management```

# Repo Guide

**Please reach out to me (Rufus Ponniah) in the groups E-H Teams channel if you are having any git/repository issues**


- Each team has a designated branch and a designated directory to begin building their component
- There is also a `shared_components` directory for shared frontend components
- Make sure you are working in the designated branch for your team, or you will not be able to push your changes back to the repo
  - if using VSCode, you can ensure you are on the right branch by going:<br> `source control (3rd icon down on the left)`->`options (3 dots top right of panel)`->`Checkout to...`->`your team's branch`
- If you want to make branches within your team to seperate features, sprints, etc, make sure that the source branch belongs to **your team**, not **main**
- It is up to you to coordinate code changes within your team. Git is pretty good, but if multiple team members make changes to the same code on there locally, then there will be conflicts pushing back to your team branch

# Merging pull requests to main
- you can merge another groups branch into your branch whenever required (e.g. I want to test my `experiments engine` using the `experiment management portal` frontend)
- Merging pull requests to main is intended to be an intra-group effort that we do in a meeting at the end of sprints
  - Currently, these pull requests must be approved by at least 3 people, including 1 maintainer. If you want to be a maintainer or want to nominate a maintainer from your team, please let me know.


