from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from models import Summary, Fan, Board, Pool, BlockEvent

STAGING_DIR = Path("/tmp/s19i-os-staging")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class MetricStore:
    def __init__(self) -> None:
        self.summary = Summary(
            uptime_sec=123456,
            state="mining",
            current_hashrate_ths=95.40,
            average_hashrate_5m_ths=94.88,
            power_w=3150,
            efficiency_jth=33.02,
            best_share=18234567890.0,
            blocks_found_total=1,
            last_found_block=BlockEvent(
                timestamp=_now(),
                height=887001,
                block_hash="000000000000000000example",
                pool_url="stratum+tcp://pool.example:3333",
                best_share_at_found=18234567890.0,
                status="confirmed",
            ),
            fans=[Fan(id=1, rpm=6120), Fan(id=2, rpm=5980), Fan(id=3, rpm=6050), Fan(id=4, rpm=6010)],
            boards=[
                Board(id=1, chips=76, temp_c=68.0, freq_mhz=520.0, voltage_mv=1320, hashrate_ths=31.8, status="ok"),
                Board(id=2, chips=76, temp_c=69.5, freq_mhz=520.0, voltage_mv=1320, hashrate_ths=31.6, status="ok"),
                Board(id=3, chips=76, temp_c=67.4, freq_mhz=520.0, voltage_mv=1320, hashrate_ths=32.0, status="ok"),
            ],
            pools=[
                Pool(id=1, url="stratum+tcp://pool.example:3333", user="wallet.worker", status="alive", active=True, accepted=10234, rejected=22, stale=3),
                Pool(id=2, url="stratum+tcp://backup.example:3333", user="wallet.worker", status="standby", active=False, accepted=0, rejected=0, stale=0),
            ],
        )
        self.blocks = [self.summary.last_found_block] if self.summary.last_found_block else []
        self.settings = {
            "target_temp_c": 70,
            "fan_mode": "auto",
            "power_profile": "normal",
            "hashing_enabled": True,
        }
        self.firmware_status = {
            "model": "Antminer S19i",
            "current_version": "S19i-OS 0.2.0",
            "state": "idle",
            "staged_filename": None,
            "staged_size": 0,
            "message": "No firmware package staged",
            "updated_at": _now(),
        }

    def get_summary(self) -> Summary:
        return self.summary

    def get_blocks(self):
        return self.blocks

    def get_best_share(self):
        return {
            "best_share": self.summary.best_share,
            "best_share_since_boot": self.summary.best_share,
            "blocks_found_total": self.summary.blocks_found_total,
            "last_found_block": self.summary.last_found_block,
        }

    def get_settings(self):
        return self.settings

    def update_settings(self, payload: dict):
        self.settings.update(payload)
        return self.settings

    def get_firmware_status(self):
        return self.firmware_status

    def validate_firmware_meta(self, payload: dict):
        target_model = payload.get("model")
        return {
            "ok": target_model in {None, "Antminer S19i"},
            "expected_model": "Antminer S19i",
            "received_model": target_model,
            "message": "Model accepted" if target_model in {None, "Antminer S19i"} else "Wrong target model",
        }

    async def stage_firmware(self, upload_file):
        STAGING_DIR.mkdir(parents=True, exist_ok=True)
        target = STAGING_DIR / upload_file.filename
        total = 0
        with target.open("wb") as f:
            while True:
                chunk = await upload_file.read(1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                f.write(chunk)

        self.firmware_status.update({
            "state": "staged",
            "staged_filename": upload_file.filename,
            "staged_size": total,
            "message": "Firmware uploaded to staging. Ready for validation/apply.",
            "updated_at": _now(),
        })
        return {"ok": True, **self.firmware_status}

    def apply_staged_firmware(self):
        if not self.firmware_status.get("staged_filename"):
            return {"ok": False, "message": "No staged firmware package"}

        self.firmware_status.update({
            "state": "apply-pending",
            "message": "Here the real S19i apply script should stop miner, switch to maintenance mode, unpack package and schedule reboot.",
            "updated_at": _now(),
        })
        return {"ok": True, **self.firmware_status}
