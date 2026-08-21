import asyncio
import grpc
import telemetry_pb2
import telemetry_pb2_grpc


class TelemetryServicer(telemetry_pb2_grpc.AnomalyDetectorServicer):
    def __init__(self, detector=None):
        if detector is None:
            from model import AnomalyDetector

            detector = AnomalyDetector()
        self.detector = detector

    async def StreamMetrics(self, request_iterator, context):
        async for metric in request_iterator:
            is_anomaly, score = await asyncio.to_thread(
                self.detector.predict,
                metric.cpu_usage,
                metric.ram_usage,
                metric.memory_usage,
                metric.container_id,
            )

            action = (
                telemetry_pb2.StatutAction.RESTART_CONTAINER
                if is_anomaly
                else telemetry_pb2.StatutAction.PASS
            )
            description = f"High MSE Loss {score}" if is_anomaly else "Normal"
            yield telemetry_pb2.AnomalyResponse(
                is_anomaly=is_anomaly,
                anomaly_score=score,
                description=description,
                action=action,
            )

    async def AnalyzeLog(self, request_iterator, context):
        await context.abort(
            grpc.StatusCode.UNIMPLEMENTED,
            "AnalyzeLog is not implemented",
        )


async def serve():
    from model import AnomalyDetector

    detector = AnomalyDetector()
    server = grpc.aio.server()
    telemetry_pb2_grpc.add_AnomalyDetectorServicer_to_server(
        TelemetryServicer(detector), server
    )
    server.add_insecure_port("[::]:50051")

    await server.start()
    print("Anomaly Detection gRPC Server active on port 50051...")
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
