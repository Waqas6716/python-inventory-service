from threading import Lock
from uuid import UUID

from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Inventory Service", version="0.1.0")
_stock = {"SKU-CHAIR-01": 12, "SKU-DESK-01": 5}
_reservations: dict[str, dict] = {}
_lock = Lock()


class ReservationRequest(BaseModel):
    sku: str = Field(min_length=3, max_length=64)
    quantity: int = Field(gt=0, le=100)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/v1/items/{sku}")
def item(sku: str) -> dict:
    if sku not in _stock:
        raise HTTPException(status_code=404, detail="item not found")
    return {"sku": sku, "available": _stock[sku]}


@app.post("/v1/reservations", status_code=status.HTTP_201_CREATED)
def reserve(payload: ReservationRequest, idempotency_key: str = Header(min_length=8)) -> dict:
    with _lock:
        if idempotency_key in _reservations:
            return _reservations[idempotency_key]
        available = _stock.get(payload.sku)
        if available is None:
            raise HTTPException(status_code=404, detail="item not found")
        if available < payload.quantity:
            raise HTTPException(status_code=409, detail="insufficient stock")
        _stock[payload.sku] -= payload.quantity
        result = {"id": str(UUID(int=len(_reservations) + 1)), "sku": payload.sku,
                  "quantity": payload.quantity, "status": "reserved"}
        _reservations[idempotency_key] = result
        return result
