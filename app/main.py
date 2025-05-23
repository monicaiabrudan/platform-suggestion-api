# To run this API, ensure you have FastAPI and Uvicorn installed:
# pip install fastapi uvicorn

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Course Platform Suggestion API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Course Platform Suggestion API. Visit /docs for interactive documentation."}

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or set to your Vercel domain for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CourseData(BaseModel):
    online_onsite: str
    location: Optional[str] = ""
    dependency_issues: Optional[str] = ""
    setup_time: Optional[str] = ""
    software_tools: Optional[str] = ""
    training_data_access: Optional[str] = ""
    pipeline_fairness: Optional[str] = ""
    data_fairness: Optional[str] = ""
    data_citability: Optional[str] = ""
    course_goals: Optional[str] = ""
    participant_demographics: Optional[str] = ""
    learning_needs: Optional[str] = ""
    need_software_installed: Optional[bool] = False
    is_software_cross_platform: Optional[bool] = True
    need_windows_os_or_license: Optional[bool] = False
    min_computer_specs_met: Optional[bool] = True
    share_vm_method: Optional[str] = ""
    can_share_vm_at_scale: Optional[bool] = True
    is_computer_mandatory: Optional[bool] = True
    is_discussion_based: Optional[bool] = False
    software_via_web_gui: Optional[bool] = False
    computer_use_note_taking_only: Optional[bool] = False
    software_free_and_compatible: Optional[bool] = True
    required_os: Optional[str] = ""
    participant_os_access: Optional[bool] = True
    can_build_linux_vm: Optional[bool] = True
    can_run_on_colab_or_cloud: Optional[bool] = True
    must_execute_on_cloud: Optional[bool] = False
    webservers_accessible: Optional[bool] = True
    has_cloud_budget: Optional[bool] = False
    can_install_on_ubuntu: Optional[bool] = True
    computer_owner: Optional[str] = "participants"
    institution_allows_software: Optional[bool] = True
    data_share_method: Optional[str] = "internet"
    internet_bandwidth_ok: Optional[bool] = True
    can_use_globus: Optional[bool] = True
    has_hpc_access: Optional[bool] = False

def suggest_platform(data: CourseData) -> str:
    online_mode = data.online_onsite.lower()
    dependency_issues = data.dependency_issues.lower()
    setup_time = data.setup_time.lower()
    training_data_access = data.training_data_access.lower()
    pipeline_fairness = data.pipeline_fairness.lower()
    data_fairness = data.data_fairness.lower()
    data_citability = data.data_citability.lower()
    course_goals = data.course_goals.lower()
    learning_needs = data.learning_needs.lower()

    if not data.is_computer_mandatory or data.is_discussion_based:
        return "No computer platform required"

    if data.computer_use_note_taking_only:
        return "Default OS Usage"

    if data.software_via_web_gui and data.webservers_accessible:
        return "Web-based GUI Platform"

    if ("online" in online_mode and
        ("no" in dependency_issues or "minor" in dependency_issues) and
        ("all" in training_data_access or "some" in training_data_access) and
        not data.need_software_installed):
        return "Google Colab"

    if ("slow" in setup_time or "moderate" in setup_time) and "onsite" in online_mode:
        return "Virtual Machine"

    if ("major" in dependency_issues or "custom" in pipeline_fairness):
        return "Docker"

    if ("all" in pipeline_fairness and "all" in data_fairness and "all" in data_citability):
        return "Cloud Platform (e.g., AWS, GCP)"

    if "diverse" in learning_needs:
        return "Google Colab"

    if data.need_software_installed and (
        not data.is_software_cross_platform or
        not data.software_free_and_compatible or
        data.need_windows_os_or_license or
        not data.participant_os_access):
        return "Virtual Machine"

    if not data.min_computer_specs_met:
        return "Virtual Machine"

    if not data.can_share_vm_at_scale or not data.internet_bandwidth_ok:
        return "Google Colab"

    if data.must_execute_on_cloud:
        return "Cloud Platform (e.g., Google Colab, AWS)"

    if data.has_cloud_budget and data.can_run_on_colab_or_cloud:
        return "Cloud Platform"

    if data.has_hpc_access:
        return "High Performance Computing (HPC)"

    return "Virtual Machine"

@app.post("/suggest_platform")
def get_suggested_platform(course: CourseData):
    try:
        suggestion = suggest_platform(course)
        return {"suggested_platform": suggestion}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
