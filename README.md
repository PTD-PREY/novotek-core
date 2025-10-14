# Novotek Core Project

Git project containing all the needed resources to start a new Ignition Project.


## Ignition Project

### Ignition notes

- Source project name : ``` novotek-core ```.

- Theme has to be selected in Designer if not done and set to `novotek-light` or `novotek-dark`.

- Before commiting to this repository, in order to make the ignition changes more visibile, run :
```bash
cd ./scripts
python ./run_before_commit.py
```

- If files are being imported directly into a client environment, run :
```bash
cd ./scripts
python ./clean_ignition_repo.py
```

## Additionnal notes

- If on commit, you have a too long filename error for git, run the following command :
`git config "--global" core.longpaths true`