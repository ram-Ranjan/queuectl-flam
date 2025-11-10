import subprocess, time, os

def run_cmd(cmd):
    print(f"\n {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout or result.stderr)

print("🚀 Starting QueueCTL automated test...\n")

run_cmd("python queuectl.py init")

run_cmd("python queuectl.py enqueue-job \"{\\\"id\\\":\\\"job_success\\\",\\\"command\\\":\\\"echo success\\\"}\"")
run_cmd("python queuectl.py enqueue-job \"{\\\"id\\\":\\\"job_fail\\\",\\\"command\\\":\\\"false\\\"}\"")

print("\n Running workers for 10s...\n")
p = subprocess.Popen(["python", "queuectl.py", "worker-start", "--count", "1"])
time.sleep(10)
p.terminate()

run_cmd("python queuectl.py status")

run_cmd("python queuectl.py dlq-list")

print("\n✅ Test complete! Check job_logs/ for detailed logs.\n")
