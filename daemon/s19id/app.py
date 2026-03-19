from __future__ import annotations

from fastapi import FastAPI, File, UploadFile

from store import MetricStore

store = MetricStore()
app = FastAPI(title="S19i-OS API", version="0.2.1")


@app.get("/api/v1/summary")
def summary():
    return store.get_summary()


@app.get("/api/v1/chains")
def chains():
    return store.get_summary().boards


@app.get("/api/v1/pools")
def pools():
    return store.get_summary().pools


@app.get("/api/v1/best-share")
def best_share():
    return store.get_best_share()


@app.get("/api/v1/blocks")
def blocks():
    return store.get_blocks()


@app.get("/api/v1/settings")
def settings_get():
    return store.get_settings()


@app.post("/api/v1/settings")
def settings_post(payload: dict):
    return store.update_settings(payload)


@app.post("/api/v1/miner/restart")
def miner_restart():
    return {"ok": True, "action": "restart"}


@app.post("/api/v1/miner/pause")
def miner_pause():
    store.update_settings({"hashing_enabled": False})
    return {"ok": True, "action": "pause"}


@app.post("/api/v1/miner/resume")
def miner_resume():
    store.update_settings({"hashing_enabled": True})
    return {"ok": True, "action": "resume"}


@app.get("/api/v1/firmware/status")
def firmware_status():
    return store.get_firmware_status()


@app.post("/api/v1/firmware/check")
def firmware_check(payload: dict):
    return store.validate_firmware_meta(payload)


@app.post("/api/v1/firmware/upload")
async def firmware_upload(file: UploadFile = File(...)):
    return await store.stage_firmware(file)


@app.post("/api/v1/firmware/apply")
def firmware_apply():
    return store.apply_staged_firmware()
