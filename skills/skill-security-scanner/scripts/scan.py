import os
import json
import sys
import time
import argparse
import requests
import zipfile
import tempfile
import shutil

# Configuration
BASE_URL = "http://127.0.0.1:8181/api/top/mana-open/cn-north-1/2025-01-01"
UPLOAD_URL = f"{BASE_URL}/UploadAndScanSkill"
DETAIL_URL = f"{BASE_URL}/GetSkillScanDetail"

# Scan Status Enum (mapped from API)
SCAN_STATUS_WAITING = "scanning"
SCAN_STATUS_RUNNING = "scanning"
SCAN_STATUS_SUCCESS = "success"
SCAN_STATUS_FAILED = "fail"
SCAN_STATUS_TIMEOUT = "timeout"

def zip_directory(dir_path):
    """Zip a directory and return the path to the temporary zip file."""
    try:
        # Create a temporary file
        temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
        temp_zip.close()
        
        with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Calculate relative path for the zip archive
                    arcname = os.path.relpath(file_path, dir_path)
                    zipf.write(file_path, arcname)
        
        return temp_zip.name
    except Exception as e:
        print(f"Error zipping directory: {e}")
        return None

def extract_data(response_json):
    """Extract Data from nested Result.Data structure."""
    if not isinstance(response_json, dict):
        return None
        
    # Handle { "Result": { "Data": { ... } } }
    if 'Result' in response_json and isinstance(response_json['Result'], dict):
        result = response_json['Result']
        if 'Data' in result:
            return result['Data']
            
    # Handle direct { "Data": { ... } } (if possible)
    if 'Data' in response_json:
        return response_json['Data']
        
    # Handle flat structure or other variations if needed
    return response_json

def upload_and_scan(name, path, description="Security scan"):
    """Upload skill zip file (or zipped folder) and start scan."""
    temp_zip_path = None
    file_to_upload = path

    try:
        if not os.path.exists(path):
            return {"error": f"Path not found: {path}"}

        # Check if path is a directory
        if os.path.isdir(path):
            temp_zip_path = zip_directory(path)
            if not temp_zip_path:
                return {"error": "Failed to zip directory"}
            file_to_upload = temp_zip_path

        files = {
            'File': (os.path.basename(file_to_upload), open(file_to_upload, 'rb'), 'application/zip')
        }
        data = {
            'Name': name,
            'Description': description
        }

        response = requests.post(UPLOAD_URL, files=files, data=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Upload failed: {str(e)}"}
    finally:
        # Cleanup temp file if created
        if temp_zip_path and os.path.exists(temp_zip_path):
            try:
                os.unlink(temp_zip_path)
            except:
                pass

def get_scan_detail(skill_id):
    """Get scan results by SkillID with polling."""
    try:
        payload = {"SkillID": skill_id}
        headers = {'Content-Type': 'application/json'}
        
        # Poll for results (max 30 seconds)
        max_retries = 100
        
        for i in range(max_retries):
            try:
                response = requests.post(DETAIL_URL, json=payload, headers=headers)
                response.raise_for_status()
                result_json = response.json()
                
                scan_data = extract_data(result_json)
                if not isinstance(scan_data, dict):
                     time.sleep(2)
                     continue

                status = scan_data.get('ScanStatus')
                
                if status == SCAN_STATUS_SUCCESS:
                    return scan_data
                elif status == SCAN_STATUS_FAILED or status == SCAN_STATUS_TIMEOUT:
                    return {"error": f"Scan failed with status: {status}", "details": scan_data.get('ScanErrMsg')}
                elif status == SCAN_STATUS_WAITING or status == SCAN_STATUS_RUNNING:
                    # Still running, wait
                    pass
                else:
                    if 'Risks' in scan_data:
                        return scan_data
            
            except Exception as e:
                pass
                
            time.sleep(20)
            
        return {"error": "Timeout waiting for scan results (10mins)"}
    except Exception as e:
        return {"error": f"Get details failed: {str(e)}"}

def main():
    parser = argparse.ArgumentParser(description="Scan OpenClaw skills via Mana Open API.")
    parser.add_argument("--name", required=True, help="Name of the skill")
    parser.add_argument("--path", required=True, help="Path to the skill directory or zip file")
    
    args = parser.parse_args()
    
    # 1. Upload and start scan
    upload_result = upload_and_scan(args.name, args.path)
    
    if "error" in upload_result:
        print(json.dumps([upload_result], indent=2))
        return

    # Extract SkillID from nested structure
    upload_data = extract_data(upload_result)
    if not upload_data:
        # Fallback to checking root if extract failed but key exists (unlikely given struct)
        skill_id = upload_result.get("SkillID")
    else:
        skill_id = upload_data.get("SkillID")
    
    if not skill_id:
        print(json.dumps([{"error": "No SkillID returned from upload", "raw": upload_result}], indent=2))
        return

    # 2. Get scan details with polling
    scan_result = get_scan_detail(skill_id)
    
    # Wrap in list for consistency
    print(json.dumps([scan_result], indent=2))

if __name__ == "__main__":
    main()
