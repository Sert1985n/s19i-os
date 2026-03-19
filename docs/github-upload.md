# Как добавить проект в GitHub

## Вариант 1. Через git

```bash
cd /path/to/s19i-os

git init -b main
git add .
git commit -m "Initial S19i-OS skeleton"

git remote add origin https://github.com/USERNAME/s19i-os.git
git push -u origin main
```

## Вариант 2. Через GitHub CLI

```bash
cd /path/to/s19i-os

git init -b main
git add .
git commit -m "Initial S19i-OS skeleton"

gh repo create s19i-os --private --source=. --remote=origin --push
```

## Ветка для разработки

```bash
git checkout -b bringup/s19i-stock-base
```

## Коммит после подключения реального miner backend

```bash
git add .
git commit -m "Connect stock S19i miner metrics backend"
git push
```
