# S19i-OS

Сlean-room каркас кастомной прошивки/надстройки для **Antminer S19i** с целевым функционалом уровня VNISH-класса продукта, но на собственной архитектуре.

## Основной путь установки и обновления

Для пользователя основной сценарий должен быть **через Web UI**: 

- страница `System -> Firmware`
- загрузка файла прошивки в браузере
- проверка модели/версии/хеша
- staging во временную папку
- переход в maintenance mode
- применение обновления
- перезапуск и проверка health

SD recovery и ручной recovery не являются штатным пользовательским путём. Они нужны только как аварийный запасной вариант на случай неудачного обновления.

## Цель

Сделать собственную систему управления майнером с такими блоками функций:

- Dashboard / Summary
- Pools / Failover
- Power profiles
- Fan / Thermal control
- Watchdog
- BestShare
- FoundBlock / Block history
- REST API + `/docs`
- Firmware update через Web UI
- GitHub-репозиторий для контроля изменений

## Что уже заложено в каркасе

- API-спецификация `api/openapi.yaml`
- демоны `s19id`, `miner_supervisor`, `thermald`, `updater`
- web UI-заглушка
- схема хранения метрик `BestShare`, `FoundBlock`, temperatures, hashrate
- черновой API для страницы обновления прошивки
- инструкция по загрузке проекта в GitHub

## Важная идея

На первом этапе лучше оставлять аппаратно-зависимый слой стокового S19i (`kernel`, board control, низкоуровневый доступ к hashboard/fan/temp), а поверх него строить свою систему управления.

## Базовая архитектура

- `daemon/s19id` — REST API и агрегатор метрик
- `daemon/miner_supervisor` — работа с майнером, пулами, конфигом, BestShare, block events
- `daemon/thermald` — thermal policy, fan logic, emergency shutdown
- `daemon/updater` — Web UI firmware update, проверка пакета, staging, progress, reboot flow
- `webui/` — своя панель
- `scripts/` — упаковка overlay / git init / release helper

## Старт

```bash
cd daemon/s19id
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8088
```

Открыть:

- API docs: `http://<HOST>:8088/docs`
- Summary: `http://<HOST>:8088/api/v1/summary`
- Firmware status: `http://<HOST>:8088/api/v1/firmware/status`

## Дальше

1. Подключить реальные данные от `bmminer`/стокового miner binary.
2. Привязать metrics store к логам/событиям майнера.
3. Подключить updater к реальному staging/apply-script под S19i.
4. Сделать штатный Web UI update как основной путь установки новых версий.
