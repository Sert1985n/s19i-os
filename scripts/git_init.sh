#!/usr/bin/env bash
set -euo pipefail

git init -b main
git add .
git commit -m "Initial S19i-OS skeleton"
echo "Теперь создайте пустой репозиторий на GitHub и выполните:"
echo "git remote add origin https://github.com/USERNAME/s19i-os.git"
echo "git push -u origin main"
