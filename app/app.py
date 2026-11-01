"""Shipment Tracker - a small Flask app used to demonstrate a Jenkins CI/CD pipeline.

Endpoints
---------
GET  /                      HTML dashboard (shows build number -> proves each deploy)
GET  /health                Health check used by the pipeline's Smoke Test stage
GET  /api/version           App version + Jenkins build number
GET  /api/shipments         List shipments
GET  /api/shipments/<id>    Get one shipment
POST /api/shipments         Create a shipment  {"origin": "...", "destination": "...", "mode": "SEA|AIR|ROAD"}
"""
import os
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template, request

APP_VERSION = "1.0.0"
# Change this line during the video demo, commit + push, and Jenkins redeploys it automatically.
WELCOME_MESSAGE = "Hello from Ashwini - deployed automatically by Jenkins"

VALID_MODES = {"SEA", "AIR", "ROAD"}

app = Flask(__name__)

SHIPMENTS = {
    "SHP-1001": {"id": "SHP-1001", "origin": "JNPT Mumbai", "destination": "Rotterdam",
                 "mode": "SEA", "status": "IN_TRANSIT"},
    "SHP-1002": {"id": "SHP-1002", "origin": "Pune", "destination": "Dubai",
                 "mode": "AIR", "status": "CUSTOMS_CLEARED"},
    "SHP-1003": {"id": "SHP-1003", "origin": "Pune", "destination": "Chennai",
                 "mode": "ROAD", "status": "DELIVERED"},
}


def build_number():
    return os.getenv("BUILD_NUMBER", "local")


@app.route("/")
def index():
    return render_template(
        "index.html",
        shipments=list(SHIPMENTS.values()),
        message=WELCOME_MESSAGE,
        version=APP_VERSION,
        build=build_number(),
        hostname=os.getenv("HOSTNAME", "local"),
    )


@app.route("/health")
def health():
    return jsonify(status="UP", time=datetime.now(timezone.utc).isoformat())


@app.route("/api/version")
def version():
    return jsonify(version=APP_VERSION, build=build_number())


@app.route("/api/shipments", methods=["GET"])
def list_shipments():
    return jsonify(count=len(SHIPMENTS), shipments=list(SHIPMENTS.values()))


@app.route("/api/shipments/<shipment_id>", methods=["GET"])
def get_shipment(shipment_id):
    shipment = SHIPMENTS.get(shipment_id.upper())
    if shipment is None:
        return jsonify(error="Shipment not found"), 404
    return jsonify(shipment)


@app.route("/api/shipments", methods=["POST"])
def create_shipment():
    data = request.get_json(silent=True) or {}
    missing = [f for f in ("origin", "destination", "mode") if not data.get(f)]
    if missing:
        return jsonify(error=f"Missing fields: {', '.join(missing)}"), 400
    mode = str(data["mode"]).upper()
    if mode not in VALID_MODES:
        return jsonify(error=f"mode must be one of {sorted(VALID_MODES)}"), 400

    new_id = f"SHP-{1001 + len(SHIPMENTS)}"
    shipment = {"id": new_id, "origin": data["origin"], "destination": data["destination"],
                "mode": mode, "status": "BOOKED"}
    SHIPMENTS[new_id] = shipment
    return jsonify(shipment), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
