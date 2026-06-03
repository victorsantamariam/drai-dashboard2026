# DRAI Dashboard - API Reference

Complete API documentation for the DRAI Dashboard backend service.

**Base URL**: `https://drai-dashboard-backend.onrender.com`  
**Version**: 1.0  
**Format**: JSON  

---

## 📋 Table of Contents

1. [Authentication](#authentication)
2. [Endpoints](#endpoints)
3. [Error Handling](#error-handling)
4. [Examples](#examples)
5. [Rate Limiting](#rate-limiting)

---

## Authentication

Currently, the API is open without authentication. For production use, implement API key or JWT authentication.

### Planned Security Measures
- API key authentication
- JWT bearer tokens
- User authentication
- Rate limiting per user

---

## Endpoints

### 1. Health Check

**Purpose**: Verify the API is running and healthy

```
GET /api/health
```

**Parameters**: None

**Response** (200 OK):
```json
{
  "status": "ok",
  "message": "Backend running"
}
```

**cURL Example**:
```bash
curl https://drai-dashboard-backend.onrender.com/api/health
```

**JavaScript Example**:
```javascript
fetch('https://drai-dashboard-backend.onrender.com/api/health')
  .then(res => res.json())
  .then(data => console.log(data));
```

---

### 2. Upload Files

**Purpose**: Upload and process DOCX/ZIP files

```
POST /api/upload
```

**Content-Type**: `multipart/form-data`

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| files | file | ✅ Yes | DOCX or ZIP files (multiple supported) |

**Supported File Types**:
- `.docx` - Microsoft Word documents (Office 2007+)
- `.zip` - ZIP archives containing DOCX files

**File Size Limits**:
- Single file: max 50MB
- Total upload: max 500MB (free tier)

**Response** (200 OK):
```json
{
  "success": true,
  "report_id": 1,
  "data": {
    "total_files": 2,
    "total_tables": 5,
    "total_activities": 1500,
    "areas": {
      "Apoyo Logístico": 750,
      "Gestión Sistemas": 300,
      "Soporte Telemático": 200,
      "Soporte INGENI@": 150,
      "Documental CENDOI": 100,
      "Gestión Proyectos": 0,
      "INGENI@": 0,
      "Producción": 0,
      "Administrativa": 0
    },
    "files_processed": [
      {
        "name": "semana_01.docx",
        "activities": 750
      },
      {
        "name": "semana_02.docx",
        "activities": 750
      }
    ]
  },
  "files": [
    {
      "filename": "semana_01.docx",
      "status": "processed"
    },
    {
      "filename": "semana_02.docx",
      "status": "processed"
    }
  ]
}
```

**Error Response** (400 Bad Request):
```json
{
  "error": "No files provided"
}
```

**Error Response** (500 Internal Server Error):
```json
{
  "error": "Error message describing what went wrong"
}
```

**cURL Example**:
```bash
# Single file
curl -X POST \
  -F "files=@semana_01.docx" \
  https://drai-dashboard-backend.onrender.com/api/upload

# Multiple files
curl -X POST \
  -F "files=@semana_01.docx" \
  -F "files=@semana_02.docx" \
  https://drai-dashboard-backend.onrender.com/api/upload

# ZIP archive
curl -X POST \
  -F "files=@semanas.zip" \
  https://drai-dashboard-backend.onrender.com/api/upload
```

**JavaScript Example**:
```javascript
const formData = new FormData();
formData.append('files', document.getElementById('file1').files[0]);
formData.append('files', document.getElementById('file2').files[0]);

fetch('https://drai-dashboard-backend.onrender.com/api/upload', {
  method: 'POST',
  body: formData
})
.then(res => res.json())
.then(data => {
  console.log(`Processed ${data.data.total_files} files`);
  console.log(`Total activities: ${data.data.total_activities}`);
})
.catch(err => console.error('Upload failed:', err));
```

**Python Example**:
```python
import requests

files = [
    open('semana_01.docx', 'rb'),
    open('semana_02.docx', 'rb')
]

response = requests.post(
    'https://drai-dashboard-backend.onrender.com/api/upload',
    files={'files': files}
)

data = response.json()
print(f"Report ID: {data['report_id']}")
print(f"Total activities: {data['data']['total_activities']}")
```

---

### 3. Get All Reports

**Purpose**: Retrieve all processed reports

```
GET /api/reports
```

**Parameters**: None

**Query Parameters**: None (future: pagination support)

**Response** (200 OK):
```json
{
  "reports": [
    {
      "id": 1,
      "timestamp": "2026-06-01T12:30:45.123456",
      "consolidated": {
        "total_files": 2,
        "total_tables": 5,
        "total_activities": 1500,
        "areas": {
          "Apoyo Logístico": 750,
          "Gestión Sistemas": 300,
          "Soporte Telemático": 200,
          "Soporte INGENI@": 150,
          "Documental CENDOI": 100,
          "Gestión Proyectos": 0,
          "INGENI@": 0,
          "Producción": 0,
          "Administrativa": 0
        },
        "files_processed": [
          {
            "name": "semana_01.docx",
            "activities": 750
          },
          {
            "name": "semana_02.docx",
            "activities": 750
          }
        ]
      },
      "files": [
        {
          "filename": "semana_01.docx",
          "status": "processed"
        },
        {
          "filename": "semana_02.docx",
          "status": "processed"
        }
      ]
    }
  ]
}
```

**cURL Example**:
```bash
curl https://drai-dashboard-backend.onrender.com/api/reports
```

**JavaScript Example**:
```javascript
fetch('https://drai-dashboard-backend.onrender.com/api/reports')
  .then(res => res.json())
  .then(data => {
    data.reports.forEach(report => {
      console.log(`Report ${report.id}: ${report.consolidated.total_activities} activities`);
    });
  });
```

---

### 4. Get Specific Report

**Purpose**: Retrieve details for a specific report

```
GET /api/reports/<id>
```

**Path Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | integer | ✅ Yes | Report ID |

**Response** (200 OK):
```json
{
  "id": 1,
  "timestamp": "2026-06-01T12:30:45.123456",
  "consolidated": {
    "total_files": 2,
    "total_tables": 5,
    "total_activities": 1500,
    "areas": {
      "Apoyo Logístico": 750,
      "Gestión Sistemas": 300,
      "Soporte Telemático": 200,
      "Soporte INGENI@": 150,
      "Documental CENDOI": 100,
      "Gestión Proyectos": 0,
      "INGENI@": 0,
      "Producción": 0,
      "Administrativa": 0
    },
    "files_processed": [
      {
        "name": "semana_01.docx",
        "activities": 750
      },
      {
        "name": "semana_02.docx",
        "activities": 750
      }
    ]
  },
  "files": [
    {
      "filename": "semana_01.docx",
      "status": "processed"
    },
    {
      "filename": "semana_02.docx",
      "status": "processed"
    }
  ]
}
```

**Error Response** (404 Not Found):
```json
{
  "error": "Report not found"
}
```

**cURL Example**:
```bash
curl https://drai-dashboard-backend.onrender.com/api/reports/1
```

**JavaScript Example**:
```javascript
const reportId = 1;
fetch(`https://drai-dashboard-backend.onrender.com/api/reports/${reportId}`)
  .then(res => res.json())
  .then(data => console.log(data));
```

---

### 5. Delete Report

**Purpose**: Remove a report from the database

```
DELETE /api/reports/<id>
```

**Path Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | integer | ✅ Yes | Report ID |

**Response** (200 OK):
```json
{
  "success": true
}
```

**Error Response** (404 Not Found):
```json
{
  "error": "Report not found"
}
```

**cURL Example**:
```bash
curl -X DELETE https://drai-dashboard-backend.onrender.com/api/reports/1
```

**JavaScript Example**:
```javascript
const reportId = 1;
fetch(`https://drai-dashboard-backend.onrender.com/api/reports/${reportId}`, {
  method: 'DELETE'
})
.then(res => res.json())
.then(data => console.log('Report deleted:', data.success));
```

---

### 6. Export Report

**Purpose**: Export a report as JSON file

```
GET /api/export/<id>
```

**Path Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | integer | ✅ Yes | Report ID |

**Response**: Full report object (same as GET /api/reports/<id>)

**Content-Type**: `application/json`

**cURL Example**:
```bash
# Download as file
curl https://drai-dashboard-backend.onrender.com/api/export/1 > report_1.json
```

**JavaScript Example**:
```javascript
const reportId = 1;
fetch(`https://drai-dashboard-backend.onrender.com/api/export/${reportId}`)
  .then(res => res.json())
  .then(data => {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `report_${reportId}.json`;
    a.click();
  });
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Common Cause |
|------|---------|-------------|
| 200 | OK | Successful request |
| 400 | Bad Request | Invalid parameters or no files provided |
| 404 | Not Found | Report doesn't exist |
| 500 | Server Error | Processing error, check backend logs |

### Error Response Format

```json
{
  "error": "Description of what went wrong"
}
```

### Common Error Messages

```json
// No files provided
{"error": "No files provided"}

// Report not found
{"error": "Report not found"}

// Processing error
{"error": "Error al procesar archivos"}

// Invalid file type
{"error": "File type not supported"}
```

---

## Examples

### Example 1: Complete Upload and Export Workflow

```bash
#!/bin/bash

API_BASE="https://drai-dashboard-backend.onrender.com"

# 1. Upload files
echo "Uploading files..."
RESPONSE=$(curl -s -X POST \
  -F "files=@semana_01.docx" \
  -F "files=@semana_02.docx" \
  "$API_BASE/api/upload")

# Extract report ID
REPORT_ID=$(echo $RESPONSE | grep -o '"report_id":[0-9]*' | grep -o '[0-9]*')
echo "Report ID: $REPORT_ID"

# 2. Retrieve report details
echo "Fetching report details..."
curl -s "$API_BASE/api/reports/$REPORT_ID" | json_pp

# 3. Export report
echo "Exporting report..."
curl -s "$API_BASE/api/export/$REPORT_ID" > "report_$REPORT_ID.json"
echo "Report saved to report_$REPORT_ID.json"
```

### Example 2: Python Integration

```python
import requests
import json
from datetime import datetime

class DRAIClient:
    def __init__(self, base_url="https://drai-dashboard-backend.onrender.com"):
        self.base_url = base_url
    
    def upload_files(self, file_paths):
        """Upload multiple files"""
        files = []
        for file_path in file_paths:
            files.append(('files', open(file_path, 'rb')))
        
        response = requests.post(
            f"{self.base_url}/api/upload",
            files=files
        )
        return response.json()
    
    def get_report(self, report_id):
        """Get report details"""
        response = requests.get(
            f"{self.base_url}/api/reports/{report_id}"
        )
        return response.json()
    
    def export_report(self, report_id, filename=None):
        """Export report as JSON"""
        if filename is None:
            filename = f"report_{report_id}_{datetime.now().isoformat()}.json"
        
        response = requests.get(
            f"{self.base_url}/api/export/{report_id}"
        )
        
        with open(filename, 'w') as f:
            json.dump(response.json(), f, indent=2)
        
        return filename

# Usage
client = DRAIClient()
result = client.upload_files(['semana_01.docx', 'semana_02.docx'])
print(f"Total activities: {result['data']['total_activities']}")

report_id = result['report_id']
report = client.get_report(report_id)
client.export_report(report_id)
```

### Example 3: JavaScript with Error Handling

```javascript
class DRAIApi {
  constructor(baseUrl = 'https://drai-dashboard-backend.onrender.com') {
    this.baseUrl = baseUrl;
  }

  async uploadFiles(files) {
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));

    try {
      const response = await fetch(`${this.baseUrl}/api/upload`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Upload failed:', error);
      throw error;
    }
  }

  async getReport(reportId) {
    const response = await fetch(`${this.baseUrl}/api/reports/${reportId}`);
    if (!response.ok) throw new Error('Report not found');
    return response.json();
  }

  async getAllReports() {
    const response = await fetch(`${this.baseUrl}/api/reports`);
    if (!response.ok) throw new Error('Failed to fetch reports');
    return response.json();
  }
}

// Usage
const api = new DRAIApi();
const input = document.getElementById('fileInput');
input.addEventListener('change', async (e) => {
  const files = Array.from(e.target.files);
  const result = await api.uploadFiles(files);
  console.log(`Processed ${result.data.total_files} files`);
});
```

---

## Rate Limiting

### Current Status
- No rate limiting implemented (free tier)

### Recommended Limits for Production
- 100 requests per minute per IP
- 10MB max file size per request
- 500MB max per day per user

### Future Implementation
Rate limiting will be added when moving to production:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1234567890
```

---

## Best Practices

1. **Batch Operations**: Use ZIP files for processing multiple documents at once
2. **Error Handling**: Always check response status and error messages
3. **Timeouts**: Set reasonable timeouts (30+ seconds) for large files
4. **Retry Logic**: Implement exponential backoff for failed requests
5. **Logging**: Log API responses for debugging and auditing
6. **Rate Limiting**: Respect rate limits once implemented

---

## Changelog

### v1.0 (2026-06-01)
- Initial API release
- File upload endpoint
- Report retrieval endpoints
- Export functionality
- CORS enabled

---

## Support

For API issues or questions:
1. Check this documentation
2. Review backend logs on Render
3. Test endpoints with cURL or Postman
4. Check browser console for client-side errors

---

**Last Updated**: June 1, 2026  
**Status**: Active ✅
