import os
from opentelemetry import metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from azure.monitor.opentelemetry.exporter import AzureMonitorMetricExporter
from dotenv import load_dotenv

load_dotenv('.env')
CONNECTION_STRING = os.getenv('CONNECTION_STRING')

resource = Resource.create({
    "service.name": "python-backend-app",
    "service.namespace": "VaysaNexus"
})

# Initialize metrics
metric_exporter = AzureMonitorMetricExporter(connection_string=CONNECTION_STRING)
metric_reader = PeriodicExportingMetricReader(metric_exporter)
metrics_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(metrics_provider)
meter = metrics.get_meter(__name__)

# Example custom metrics
request_counter = meter.create_counter(
    "chat_requests_total",
    description="Total number of chat requests"
)

token_counter = meter.create_counter(
    "tokens_generated_total",
    description="Total tokens generated"
)

def get_meter():
    return meter, request_counter, token_counter
