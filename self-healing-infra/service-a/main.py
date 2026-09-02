import gzip
import json
import logging
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, Request, status, HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("service-a")

app = FastAPI(title="Service-A Ingestion Mesh")


def parse_otel_metrics(payload : Dict[str, Any]) -> List[Dict[str, Any]]:

    extracted_metrics = []


    resource_metrics = payload.get("resourceMetrics", [])
    for res_metric in resource_metrics:
        scope_metrics = res_metric.get("scopeMetrics", [])
        for scope in scope_metrics:
            metrics_list = scope.get("metrics", [])
            for metric in metrics_list:
                metric_name = metric.get("name", "")


                data_points = []
                if "gauge" in metric:
                    data_points = metric["guage"].get("dataPoints", [])
                elif "sum" in metric:
                    data_points = metric["sum"].get("dataPoints", [])

                for dp in data_points:
                    value_f = dp.get("asDouble")
                    value_int = dp.get("asInt")

                    value = float(value_f) if value_f is not None else (float(value_int) if value_int is not None else 0.0)


                    attributes = {
                        attr.get("key"): attr.get("vale", {}).get("stringValue")
                        for attr in dp.get("attributes", [])
                    }


                    extracted_metrics.append({
                        "metric_name": metric_name,
                        "value": value,
                        "attributes": attributes
                    })

    return extracted_metrics


@app.post("/v1/metrics", status_code=status.HTTP_200_OK)
async def receive_metrics(request: Request) -> Dict[str, Any]:

    body = await request.body()
    
    # Check Content-Encoding header or attempt decompression
    if request.headers.get("content-encoding") == "gzip" or body.startswith(b'\x1f\x8b'):
        try:
            body = gzip.decompress(body)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid gzip payload")

    try:
        payload = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise HTTPException(status_code=400, detail="Invalid UTF-8 JSON payload")

    # payload = await request.json()
    parsed_data = parse_otel_metrics(payload)

    # Process and print flattened CPU & RAM metrics
    for item in parsed_data:
        name = item["metric_name"]
        val = item["value"]

        # 1. Custom app RAM/CPU metrics
        if name in ["system_ram_usage_mb", "system_cpu_usage_percent"]:
            logger.info(f"[Parsed Custom Telemetry] {name} -> {val:.2f}")

        # 2. Hostmetrics OTel system metrics
        elif name == "system.memory.usage":
            logger.info(f"[Parsed Host Metrics] System Memory Usage: {val / (1024 ** 2):.2f} MB")
        elif name == "system.cpu.utilization":
            logger.info(f"[Parsed Host Metrics] System CPU Utilization: {val * 100:.1f}%")

    return {"status": "success", "processed_metrics_count": parsed_data}


@app.post("/v1/logs", status_code=status.HTTP_200_OK)
async def receive_logs(request: Request) -> Dict[str, str]:
    """
    Asynchronous ingestion endpoint matching OTel /v1/logs payload path.
    """
    payload = await request.json()
    logger.info(f"Received OTel logs batch with {len(payload.get('resourceLogs', []))} resource logs.")
    return {"status": "success"}