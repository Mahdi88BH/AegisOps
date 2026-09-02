from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader


# 1. Configure an OTLP Exporter pointing to the Otel Collector
exporter = OTLPMetricExporter(endpoint="localhost:4317", insecure=True)
# Pass the Metric to the Exporter base on an interval of time
reader = PeriodicExportingMetricReader(exporter=exporter, export_interval_millis=5000)

# 2. Set up MeterProvider
provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)

meter = metrics.get_meter("my-app_meter")

# 3. Create a metric Instrument
RAM_Usage = meter.create_counter(
    name="system_ram_usage_mb" ,
    description="Current RAm Usage in MB",
    unit="MB",
)

CPU_Usage = meter.create_counter(
    name="system_cpu_usage_percent" ,
    description="Current System CPU Usage percenr",
    unit="%",
)