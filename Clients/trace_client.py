import os
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from dotenv import load_dotenv

load_dotenv('.env')
CONNECTION_STRING = os.getenv('CONNECTION_STRING')

# Define the trace resource (for Application Map)
resource = Resource.create({
    "service.name": "python-backend-app",
    "service.namespace": "VaysaNexus",
    "deployment.environment": "dev"
})

# Initialize tracing
trace_provider = TracerProvider(resource=resource)
trace_exporter = AzureMonitorTraceExporter(connection_string=CONNECTION_STRING)
trace_provider.add_span_processor(BatchSpanProcessor(trace_exporter))

trace.set_tracer_provider(trace_provider)
tracer = trace.get_tracer(__name__)

def get_tracer():
    return tracer
