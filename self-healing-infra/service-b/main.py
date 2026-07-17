import grpc
from concurrent import futures
import time
import asyncio
from model import AnomalyDetector 
import telemetry_pb2
import telemetry_pb2_grpc

class TelemetryServicer(telemetry_pb2_grpc.AnomalyDetectorServicer):
    async def StreamMetrics(self, request_iterator, context):
        detector = AnomalyDetector()
        async for metric in request_iterator :
            isanomaly , score  = await asyncio.to_thread(detector.predict,
                metric.cpu_usage,
                metric.ram_usage , 
                metric.memory_usage
            )

            action = "RESTART_CONTAINER" if isanomaly else "PASS"
            description = f"High MSE Loss {score}" if isanomaly else "Normal"
            yield telemetry_pb2.AnomalyResponse(
                is_anomaly = isanomaly,
                anomaly_score = score,
                description = description,
                action = action
            )
    async def AnalyzeLog(self, request_iterator, context):
        async for log in request_iterator:
            yield telemetry_pb2.MetricPayload(
                cpu_usage=0.0,
                ram_usage=0.0,
                memory_usage=0.0,
                timestamp=log.timestamp
            )

async def serve():
    server = grpc.aio.server()
    telemetry_pb2_grpc.add_AnomalyDetectorServicer_to_server(TelemetryServicer(), server)
    server.add_insecure_port('[::]:50051')
    
    await server.start()
    print("Anomaly Detection gRPC Server active on port 50051...")
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())



