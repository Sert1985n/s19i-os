# Архитектура S19i-OS

## 1. Цель

Получить собственную прошивку/надстройку для Antminer S19i с функциями:

- overview dashboard
- board/chip telemetry
- pool management
- fan policy
- watchdog
- best share
- found block history
- power profiles
- autotune-v1

## 2. Основные сервисы

### s19id
REST API, сбор состояния, агрегация метрик, выдача данных в web UI.

### miner_supervisor
Запускает/перезапускает miner binary, читает статистику, следит за pool state, фиксирует BestShare и события найденного блока.

### thermald
Отдельная логика вентиляторов, защит, target temp, аварийного стопа.

## 3. Метрики

- current_hashrate_ths
- average_hashrate_5m_ths
- power_w
- efficiency_jth
- best_share
- blocks_found_total
- last_found_block_height
- last_found_block_time
- fans[]
- boards[]
- pools[]
- uptime_sec

## 4. Событие Found Block

Нужно хранить:

- timestamp
- height
- pool url
- difficulty/network target snapshot
- worker / miner id
- best_share_at_found_time
- block_hash (если доступен)
- status: pending/confirmed/orphan

## 5. BestShare

BestShare считается как максимальное значение share difficulty за период:

- since boot
- since last reset
- optionally 24h

## 6. Первичный план интеграции

1. Оставить стоковый низкоуровневый слой S19i.
2. Завести свой supervisor рядом со stock miner.
3. Считать stats по API/log/socket.
4. Вывести собственную панель и API.
5. Лишь потом переходить к более глубокому тюнингу.
