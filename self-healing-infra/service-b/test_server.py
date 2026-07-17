import pytest
import pytest_asyncio
import grpc
import asyncio
from unittest.mock import patch

import telemetry_pb2
import telemetry_pb2_grpc
from main import TelemetryServicer 

@pytest_asyncio.fixture
async def grpc_server():
    with patch('main.AnomalyDetector') as MockDetector:
        mock_instance = MockDetector.return_value
        mock_instance.predict.return_value = (True, 0.089)

        server = grpc.aio.server()
        telemetry_pb2_grpc.add_AnomalyDetectorServicer_to_server(TelemetryServicer(), server)
        
        port = server.add_insecure_port('localhost:0')
        await server.start()
        
        yield f'localhost:{port}'
        
        await server.stop(grace=None)

@pytest.mark.asyncio
async def test_stream_metrics(grpc_server):
    async with grpc.aio.insecure_channel(grpc_server) as channel:
        stub = telemetry_pb2_grpc.AnomalyDetectorStub(channel)
        
        async def generate_test_requests():
            yield telemetry_pb2.MetricPayload(
                cpu_usage=99.9,
                ram_usage=99.9,
                memory_usage=99.9,
                timestamp=1620000000
            )
            yield telemetry_pb2.MetricPayload(
                cpu_usage=85.0,
                ram_usage=90.0,
                memory_usage=80.0,
                timestamp=1620000001
            )

        call = stub.StreamMetrics(generate_test_requests())
        
        responses = []
        async for response in call:
            responses.append(response)
            
        assert len(responses) == 2
        
        assert responses[0].is_anomaly is True
        assert responses[0].anomaly_score == pytest.approx(0.089)
        assert responses[0].action == "RESTART_CONTAINER"
        assert responses[0].description == "High MSE Loss 0.089"