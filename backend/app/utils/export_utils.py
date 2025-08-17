# CSV/JSON/XML/PDF export
# backend/app/utils/export_utils.py
from __future__ import annotations
from io import BytesIO
from typing import Iterable, List, Dict, Optional
from datetime import date, datetime
from sqlalchemy import func

import pandas as pd
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from sqlalchemy.orm import Session
from ..models import WeatherHistory


# -------- helpers: fetch + normalize --------

EXPORT_COLUMNS = [
    "id", "location_name", "latitude", "longitude",
    "start_date", "end_date",
    "temperature", "humidity", "recorded_at",
    "created_at", "updated_at",
]

def _row_to_dict(row: WeatherHistory) -> Dict:
    return {
        "id": row.id,
        "location_name": row.location_name,
        "latitude": row.latitude,
        "longitude": row.longitude,
        "start_date": row.start_date.isoformat() if row.start_date else None,
        "end_date": row.end_date.isoformat() if row.end_date else None,
        "temperature": row.temperature,
        "humidity": row.humidity,
        "recorded_at": row.recorded_at.isoformat() if row.recorded_at else None,
        "created_at": row.created_at.isoformat() if row.created_at else None,
        "updated_at": row.updated_at.isoformat() if row.updated_at else None,
        # keep weather_data out by default (can be huge)
    }

def fetch_history(
    db: Session,
    location_name: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = 1000,
    skip: int = 0,
) -> List[WeatherHistory]:
    q = db.query(WeatherHistory)
    if location_name:
        # case-insensitive partial match on location_name
        q = q.filter(func.lower(WeatherHistory.location_name).like(f"%{location_name.lower()}%"))
    if start_date:
        q = q.filter(WeatherHistory.start_date >= start_date)
    if end_date:
        q = q.filter(WeatherHistory.end_date <= end_date)
    q = q.order_by(WeatherHistory.id.desc()).offset(skip).limit(limit)
    return q.all()

def to_dataframe(rows: Iterable[WeatherHistory]) -> pd.DataFrame:
    data = [_row_to_dict(r) for r in rows]
    df = pd.DataFrame(data, columns=EXPORT_COLUMNS)
    return df


# -------- exporters --------

def export_csv(rows: Iterable[WeatherHistory]) -> bytes:
    df = to_dataframe(rows)
    buf = BytesIO()
    df.to_csv(buf, index=False)
    return buf.getvalue()

def export_json(rows: Iterable[WeatherHistory]) -> bytes:
    df = to_dataframe(rows)
    buf = BytesIO()
    buf.write(df.to_json(orient="records", force_ascii=False).encode("utf-8"))
    return buf.getvalue()

def export_xml(rows: Iterable[WeatherHistory]) -> bytes:
    # simple handcrafted XML (no extra deps)
    items = [_row_to_dict(r) for r in rows]
    def esc(s: Optional[str]) -> str:
        if s is None: return ""
        return (str(s)
                .replace("&","&amp;")
                .replace("<","&lt;")
                .replace(">","&gt;")
                .replace('"',"&quot;")
                .replace("'","&apos;"))
    parts = ['<?xml version="1.0" encoding="UTF-8"?>', "<weather_history>"]
    for it in items:
        parts.append("  <record>")
        for k in EXPORT_COLUMNS:
            v = it.get(k, "")
            parts.append(f"    <{k}>{esc(v)}</{k}>")
        parts.append("  </record>")
    parts.append("</weather_history>")
    return "\n".join(parts).encode("utf-8")

def export_pdf(rows: Iterable[WeatherHistory], title: str = "Weather History Export") -> bytes:
    df = to_dataframe(rows)
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=landscape(A4), leftMargin=24, rightMargin=24, topMargin=24, bottomMargin=24)

    styles = getSampleStyleSheet()
    flow = [Paragraph(title, styles["Title"]), Spacer(1, 8)]

    # limit rows for PDF readability; CSV/JSON/XML are for bulk
    max_rows = 200
    if len(df) > max_rows:
        df = df.head(max_rows)
        flow.append(Paragraph(f"Showing first {max_rows} rows", styles["Italic"]))
        flow.append(Spacer(1, 6))

    # build table
    table_data = [EXPORT_COLUMNS] + df[EXPORT_COLUMNS].values.tolist()
    # stringify Nones
    table_data = [[("" if v is None else str(v)) for v in row] for row in table_data]

    tbl = Table(table_data, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#f2f2f2")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.black),
        ("GRID", (0,0), (-1,-1), 0.3, colors.HexColor("#cccccc")),
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 10),
        ("FONTSIZE", (0,1), (-1,-1), 9),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#fafafa")]),
    ]))

    flow.append(tbl)
    doc.build(flow)
    return buf.getvalue()
