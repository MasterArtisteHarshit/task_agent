
from fastapi import FastAPI, HTTPException
from typing import Optional
import os
from functions import get_task_output, count_days, extract_dayname, extract_package, get_correct_pkgname
import subprocess

# Initialize FastAPI app
app = FastAPI()

# Load API token
AIPROXY_TOKEN = None
try:
    with open(".env") as f:
        for line in f:
            if line.strip():
                key, value = line.strip().split("=", 1)
                if key == "AIPROXY_TOKEN":
                    AIPROXY_TOKEN = value
                    break
    if not AIPROXY_TOKEN:
        AIPROXY_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjMwMDIxMDFAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.tza4mjIp6hmedrE8AN7T5fp17gsItnTSANREHWVxIzc"
except Exception as e:
    print(f"Error loading .env: {e}")
    AIPROXY_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjMwMDIxMDFAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.tza4mjIp6hmedrE8AN7T5fp17gsItnTSANREHWVxIzc"

@app.get("/read")
async def read_file(path: str):
    if not path.startswith("/data"):
        raise HTTPException(status_code=403, detail="Access to file is not allowed")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File is not found")
    try:
        with open(path, "r") as file:
            content = file.read()
        return {"content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/run")
async def run_task(task: str):
    try:
        # Get LLM guidance for task execution
        task_output = get_task_output(AIPROXY_TOKEN, task)
        task = task.lower()

        # Handle different task types
        if "count" in task:
            # Handle counting days
            day = extract_dayname(task)
            if day:
                count_days(day)
                return {"status": "success", "task_output": task_output}

        elif "install" in task:
            # Handle package installation
            pkgname = extract_package(task)
            if pkgname:
                correct_package = get_correct_pkgname(pkgname)
                if correct_package:
                    subprocess.run(["pip", "install", correct_package])
                    return {"status": "success", "task_output": task_output}
                else:
                    raise HTTPException(status_code=404, detail="Package not found")

        elif "sort" in task and "contact" in task:
            # Handle contact sorting
            from sort_contacts import sort_contacts
            sort_contacts()
            return {"status": "success", "task_output": task_output}

        elif "log" in task and "recent" in task:
            # Handle recent logs
            from get_recent_logs import get_recent_logs
            get_recent_logs()
            return {"status": "success", "task_output": task_output}

        # Default response for unrecognized tasks
        return {
            "status": "error",
            "detail": "Task not recognized or not implemented",
            "task_output": task_output
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
