# QueueCTL  
*A CLI-based background job queue system with retry logic, DLQ management, and persistent storage.*

---

## Overview

**QueueCTL** is a production-style **CLI-based background job queue system**.  
It manages background jobs, runs multiple worker threads in parallel, retries failed jobs with exponential backoff, and moves permanently failed ones to a **Dead Letter Queue (DLQ)**.  

All data persists in a lightweight **SQLite** database, and every job run is logged separately for better traceability.

---

## Features

 - Enqueue and manage background jobs  
 - Run multiple worker processes in parallel  
 - Automatic retry with exponential backoff  
 - Dead Letter Queue (DLQ) for permanently failed jobs  
 - Persistent job storage using SQLite  
 - Configuration management via CLI  
 - Per-job logging system  
 - Automated test script for full workflow validation  

---

## Tech Stack

- **Language:** Python 3.7+  
- **Libraries:** Standard Library (sqlite3, threading, logging)  
- **Persistence:** SQLite  
- **CLI Framework:** argparse  
- **Parallelism:** Python threading  

---

## Architecture Overview

Each job follows this lifecycle:

| State | Description |
|--------|--------------|
| `pending` | Waiting to be picked by a worker |
| `processing` | Currently being executed |
| `completed` | Successfully executed |
| `failed` | Failed, retryable |
| `dead` | Permanently failed, moved to DLQ |

### Job Structure
```json
{
  "id": "unique-job-id",
  "command": "echo 'Hello World'",
  "state": "pending",
  "attempts": 0,
  "max_retries": 3,
  "created_at": "2025-11-04T10:30:00Z",
  "updated_at": "2025-11-04T10:30:00Z"
}
```

### Retry Mechanism
```
delay = backoff_base ^ attempts
```

Jobs that exceed `max_retries` are automatically moved to the Dead Letter Queue.

---

## ⚙️ Setup Instructions

```bash
# Clone repo
git clone https://github.com/<your-username>/QueueCTL.git
cd QueueCTL

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# No external dependencies required (uses standard library)
```

---

## 🚀 Usage Guide

### Initialize Database

```bash
python queuectl.py init
```

### Enqueue Jobs

```bash
python queuectl.py enqueue-job '{"id":"job1","command":"echo Hello World"}'
python queuectl.py enqueue-job '{"id":"job2","command":"false"}'
```

### Start Workers

```bash
# Start 2 worker threads
python queuectl.py worker-start --count 2
```

### Check System Status

```bash
python queuectl.py status
```

**Example Output:**
```
📊 Queue Status:
- Pending: 5
- Processing: 2
- Completed: 10
- Failed: 1
- Dead: 0
```

### View Dead Letter Queue

```bash
python queuectl.py dlq-list
```

### Retry Failed Jobs

```bash
python queuectl.py dlq-retry job2
```

---

## 📝 Configuration

The system uses `config.json` for runtime configuration:

```json
{
  "max_retries": 3,
  "backoff_base": 2
}
```

### Configuration Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `max_retries` | Maximum retry attempts before DLQ | 3 |
| `backoff_base` | Base value for exponential backoff | 2 |

You can modify configuration via CLI or by editing `config.json` directly.

---

## 🧪 Testing

### Run Automated Tests

```bash
python test_script.py
```

### Test Workflow

The test script will:

1. Initialize the database
2. Enqueue one successful and one failing job
3. Start a worker for 10 seconds
4. Display status and DLQ summary

### Expected Output

```
✅ job_success -> Completed
⚠️ job_fail failed. Retrying...
❌ job_fail moved to DLQ
```

---

## 📁 Project Structure

```
QueueCTL/
├── queuectl.py          # Main CLI application
├── test_script.py       # Automated test suite
├── config.json          # Runtime configuration
├── requirements.txt     # Python dependencies (if any)
├── README.md            # This file
├── jobs.db              # SQLite database (auto-generated)
└── job_logs/            # Job execution logs (auto-generated)
    ├── job1.log
    └── job2.log
```

---

## 🎯 Design Decisions

### Assumptions

- SQLite provides sufficient persistence for the use case
- CLI-only interface meets requirements
- Standard library components are adequate

### Trade-offs

| Decision | Rationale |
|----------|-----------|
| **Threading vs Multiprocessing** | Simpler implementation, easier debugging |
| **No External Message Broker** | Keeps system lightweight and self-contained |
| **Synchronous Retry Delays** | Easier to debug and validate behavior |
| **SQLite over PostgreSQL** | No external dependencies, simpler deployment |

---

## ✅ Implementation Checklist

| Requirement | Status |
|------------|--------|
| Job enqueue & management | ✅ |
| Multiple workers | ✅ |
| Retry with exponential backoff | ✅ |
| Dead Letter Queue | ✅ |
| Persistent storage | ✅ |
| CLI configuration | ✅ |
| Job logging | ✅ |
| Automated testing | ✅ |

---

## 🔮 Future Enhancements

- Web-based dashboard for monitoring
- Support for job priorities
- Job scheduling capabilities
- Metrics and analytics
- Docker containerization
- Support for distributed workers

---



## 👤 Author

**Ranjan Kumar**  
📧 
🔗 [GitHub](https://github.com/ram-Ranjan/) | [LinkedIn](https://www.linkedin.com/in/ranjan-kumar-6618bb163/)

---

## 🙏 Acknowledgments

Built as part of the Backend Developer Internship Assignment.

**Note:** This project demonstrates understanding of:
- Job queue architecture
- Concurrent processing
- Error handling and retry logic
- Persistent storage
- CLI application development