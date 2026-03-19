from __future__ import annotations

from pydantic import BaseModel, Field
from typing import List, Optional


class Fan(BaseModel):
    id: int
    rpm: int


class Pool(BaseModel):
    id: int
    url: str
    user: str
    status: str
    active: bool = False
    accepted: int = 0
    rejected: int = 0
    stale: int = 0


class Board(BaseModel):
    id: int
    chips: int
    temp_c: float
    freq_mhz: float
    voltage_mv: int
    hashrate_ths: float
    status: str


class BlockEvent(BaseModel):
    timestamp: str
    height: Optional[int] = None
    block_hash: Optional[str] = None
    pool_url: Optional[str] = None
    best_share_at_found: Optional[float] = None
    status: str = "pending"


class Summary(BaseModel):
    model: str = "Antminer S19i"
    firmware: str = "S19i-OS 0.1.0"
    uptime_sec: int
    state: str
    current_hashrate_ths: float
    average_hashrate_5m_ths: float
    power_w: int
    efficiency_jth: float
    best_share: float
    blocks_found_total: int
    last_found_block: Optional[BlockEvent] = None
    fans: List[Fan] = Field(default_factory=list)
    boards: List[Board] = Field(default_factory=list)
    pools: List[Pool] = Field(default_factory=list)
