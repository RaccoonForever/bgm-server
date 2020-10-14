# Board Game Mate Server

## Release process
- Create a new branch with sw-[versionID]
- Modify the version in docker-compose.yml
- Commit and push all your changes
- Create a pull request for this branch
- When the release is done (tests and devs are ok), build the image with a new tag and push it to dockerhub.io

## Useful commands
### Docker
- Adding user to group docker (works if the group has already been created): newgrp docker 
- Building an image: docker build -t raccoonforever/bgm-server:latest .
- Running a container: docker run -d -it -p 8080:80 raccoonforever/bgm-server:latest
- Enter a container running: docker exec -it [containerID] bash

### Pipenv
- Specify python version : pipenv install --python 2.7
- Remove pipenv (you should be in the directory): pipenv --rm

## Releases
### v0.0.2
- Adding more details in API response
- Adding some tests accordingly

### v0.0.1
- First release
- API working /kingdomino/predict/latest
- Inference working
- Returning only the score for an image