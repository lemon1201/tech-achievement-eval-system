from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ConstraintProfile(BaseModel):
    deadline_days: Optional[int] = None
    budget_level: Optional[str] = "medium"
    compliance_level: Optional[str] = "medium"


class Material(BaseModel):
    type: str
    content: str


class TaskInput(BaseModel):
    task_id: str = Field(default="task-temp")
    title: str
    industry: Optional[str] = "unknown"
    description: str
    constraints: ConstraintProfile = Field(default_factory=ConstraintProfile)
    materials: List[Material] = Field(default_factory=list)


class ClassifiedTask(BaseModel):
    industry: str
    task_type: str
    object_type: str
    confidence: float


class CaseHit(BaseModel):
    case_id: str
    score: float
    title: str


class RetrieveCasesRequest(BaseModel):
    industry: str
    task_type: str = "evaluation_outline"
    top_n: int = 5


class RetrieveCasesResponse(BaseModel):
    cases: List[CaseHit]


class ExtractModulesRequest(BaseModel):
    case_ids: List[str]
    module_types: List[str] = Field(default_factory=lambda: ["scope", "metrics", "methods", "thresholds", "conditions", "acceptance_rules", "evidence_rules"])
    task_profile: Dict[str, Any] = Field(default_factory=dict)


class ModuleCandidate(BaseModel):
    module_id: str
    module_type: str
    content: Dict[str, Any]
    applicability: Dict[str, Any]
    provenance: Dict[str, Any]


class ExtractModulesResponse(BaseModel):
    candidates: Dict[str, List[ModuleCandidate]]


class SelectModulesRequest(BaseModel):
    task_profile: Dict[str, Any]
    candidates: Dict[str, List[ModuleCandidate]]
    weights: Dict[str, float]


class SelectModulesResponse(BaseModel):
    selected: Dict[str, Dict[str, Any]]
    explanations: List[str]


class GenerateOutlineRequest(BaseModel):
    task_id: str
    title: str
    selected_modules: List[ModuleCandidate]


class OutlineSection(BaseModel):
    name: str
    content: str


class ValidateIssue(BaseModel):
    field: str
    severity: str
    suggestion: str


class ValidateOutlineResponse(BaseModel):
    passed: bool
    issues: List[str]
    gap_report: List[ValidateIssue]


class GeneratedOutline(BaseModel):
    task_id: str
    outline_id: str
    title: str
    sections: List[OutlineSection]
    selected_modules: List[str]
    consistency_check: Dict[str, Any]
    gap_report: List[ValidateIssue]


class EvaluateRequest(BaseModel):
    title: str
    text: str


class ExportOutlineRequest(BaseModel):
    outline: GeneratedOutline
    base_name: str = "generated_outline"
    export_dir: str = "data/processed/exports"


class ExportOutlineResponse(BaseModel):
    word_path: str
    pdf_path: str
    note: str


class EvaluateResponse(BaseModel):
    title: str
    extracted_items: List[Dict[str, Any]]
    graph_edges: List[Dict[str, Any]]
    score: float
    level: str
    reason: str
