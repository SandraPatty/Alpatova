как создать ssh ключ:
ssh-keygen -t ed25519 -C "your_email@example.com"
> Generating public/private ed25519 key pair.
> Enter a file in which to save the key (/Users/you/.ssh/id_ed25519): [Press enter]
как добавить ключ в аккаунт на GitHub
eval "$(ssh-agent -s)"
> Agent pid 59566
$ ssh-add ~/.ssh/id_ed25519
как склонировать репозиторий
git clone git@github.com:username/repository.git