import os
import logging
from opentelemetry import _logs
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from azure.monitor.opentelemetry.exporter import AzureMonitorLogExporter
from dotenv import load_dotenv

load_dotenv('.env')
CONNECTION_STRING = os.getenv('CONNECTION_STRING')

resource = Resource.create({
    "service.name": "python-backend-app",
    "service.namespace": "VaysaNexus"
})

# Initialize log provider
logger_provider = LoggerProvider(resource=resource)
log_exporter = AzureMonitorLogExporter(connection_string=CONNECTION_STRING)
logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
_logs.set_logger_provider(logger_provider)

# Standard Python logging integration
handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)

logger = logging.getLogger("AzureAppLogger")

def get_logger():
    return logger
