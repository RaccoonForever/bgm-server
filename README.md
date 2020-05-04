# Board Game Mate Server

## Useful commands
### Docker
- Adding user to group docker (works if the group has already been created): newgrp docker 
- Building an image: docker build -t raccoonforever/bgm-server:last .
- Running a container: docker run -d -it raccoonforever/bgm-server:last
- Enter a container running: docker exec -it [containerID] bash

### Pipenv
- Specify python version : pipenv install --python 2.7
- Remove pipenv (you should be in the directory): pipenv --rm

