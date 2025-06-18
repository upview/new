"""Integration tests for OpenHTF report import functionality."""

import json
import os
import random
import tempfile
from pathlib import Path

import pytest

from tofupilot import TofuPilotClient


@pytest.fixture
def test_data_dir():
    """Get the test data directory from QA examples."""
    return Path(__file__).parent.parent.parent / "tmp" / "examples" / "qa" / "client"


@pytest.mark.integration
def test_create_run_from_openhtf_report_basic(client: TofuPilotClient):
    """Create OpenHTF test, save to JSON, import to TofuPilot."""
    # Simulate OpenHTF test result structure
    serial_number = f"QA-{random.randint(100000, 999999)}"
    part_number = "PCB-001"
    
    # Create OpenHTF-style test result
    openhtf_result = {
        "dut_id": serial_number,
        "start_time_millis": 1640995200000,  # Example timestamp
        "end_time_millis": 1640995205000,
        "outcome": "PASS",
        "metadata": {
            "part_number": part_number,
            "procedure_version": "1.0.0"
        },
        "phases": [
            {
                "name": "Power Test",
                "outcome": "PASS",
                "start_time_millis": 1640995201000,
                "end_time_millis": 1640995203000,
                "measurements": {
                    "voltage": {
                        "name": "voltage",
                        "measured_value": {
                            "numeric_value": 5.1
                        },
                        "dimensions": [
                            {
                                "suffix": "V"
                            }
                        ],
                        "validators": [
                            {
                                "range": {
                                    "minimum": 4.5,
                                    "maximum": 5.5
                                }
                            }
                        ]
                    }
                }
            },
            {
                "name": "Communication Test",
                "outcome": "PASS", 
                "start_time_millis": 1640995203000,
                "end_time_millis": 1640995205000,
                "measurements": {
                    "status": {
                        "name": "status",
                        "measured_value": {
                            "text_value": "OK"
                        }
                    }
                }
            }
        ]
    }
    
    # Save to temporary JSON file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(openhtf_result, f, indent=2)
        temp_file_path = f.name
    
    try:
        # Import the OpenHTF report
        with open(temp_file_path, 'rb') as f:
            file_content = f.read()
        
        import_response = client.run_create_from_file(
            file=file_content,
            importer="openhtf"
        )
        
        assert import_response is not None
        assert hasattr(import_response, 'id')
        
    finally:
        # Clean up temporary file
        os.unlink(temp_file_path)


@pytest.mark.integration
def test_create_run_from_openhtf_report_with_attachments(client: TofuPilotClient, test_data_dir):
    """Create OpenHTF test with attachments, save to JSON, import to TofuPilot."""
    serial_number = f"QA-{random.randint(100000, 999999)}"
    part_number = "PCB-001"
    
    # Get attachment file paths
    attachment_dir = test_data_dir / "create_run_from_openhtf_report" / "with_attachments" / "data"
    jpeg_file = attachment_dir / "oscilloscope.jpeg"
    txt_file = attachment_dir / "sample_file.txt"
    
    # Verify files exist
    assert jpeg_file.exists(), f"JPEG file not found: {jpeg_file}"
    assert txt_file.exists(), f"Text file not found: {txt_file}"
    
    # Read file contents and encode as base64 (typical OpenHTF attachment format)
    import base64
    
    with open(jpeg_file, 'rb') as f:
        jpeg_content = base64.b64encode(f.read()).decode('utf-8')
    
    with open(txt_file, 'rb') as f:
        txt_content = base64.b64encode(f.read()).decode('utf-8')
    
    # Create OpenHTF-style test result with attachments
    openhtf_result = {
        "dut_id": serial_number,
        "start_time_millis": 1640995200000,
        "end_time_millis": 1640995210000,
        "outcome": "PASS",
        "metadata": {
            "part_number": part_number,
            "procedure_version": "1.0.0"
        },
        "phases": [
            {
                "name": "Signal Analysis",
                "outcome": "PASS",
                "start_time_millis": 1640995201000,
                "end_time_millis": 1640995205000,
                "measurements": {
                    "frequency": {
                        "name": "frequency",
                        "measured_value": {
                            "numeric_value": 1000.0
                        },
                        "dimensions": [
                            {
                                "suffix": "Hz"
                            }
                        ]
                    }
                },
                "attachments": [
                    {
                        "name": "oscilloscope.jpeg",
                        "data": jpeg_content,
                        "mimetype": "image/jpeg"
                    }
                ]
            },
            {
                "name": "Data Validation",
                "outcome": "PASS",
                "start_time_millis": 1640995205000,
                "end_time_millis": 1640995210000,
                "measurements": {
                    "data_integrity": {
                        "name": "data_integrity",
                        "measured_value": {
                            "boolean_value": True
                        }
                    }
                },
                "attachments": [
                    {
                        "name": "sample_file.txt",
                        "data": txt_content,
                        "mimetype": "text/plain"
                    }
                ]
            }
        ]
    }
    
    # Save to temporary JSON file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(openhtf_result, f, indent=2)
        temp_file_path = f.name
    
    try:
        # Import the OpenHTF report
        with open(temp_file_path, 'rb') as f:
            file_content = f.read()
        
        import_response = client.run_create_from_file(
            file=file_content,
            importer="openhtf"
        )
        
        assert import_response is not None
        assert hasattr(import_response, 'id')
        
    finally:
        # Clean up temporary file
        os.unlink(temp_file_path)