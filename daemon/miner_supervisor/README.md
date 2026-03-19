# miner_supervisor

Здесь должен жить модуль, который подключается к реальному miner backend S19i.

## Что он должен уметь

- запуск/рестарт `bmminer` или другого выбранного miner binary
- чтение telemetry/stat API
- парсинг share-событий
- фиксация `BestShare`
- фиксация `FoundBlock`
- определение pool state / failover
- запись metrics в `s19id`

## События, которые надо ловить

- new share accepted
- new best share
- block found / solve candidate
- chain lost
- temp critical
- fan fault
- pool dead / alive
