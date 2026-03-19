from __future__ import annotations

from fastapi import FastAPI, HTTPException

from taes.models.schemas import (
    ClassifiedTask,
    EvaluateRequest,
    EvaluateResponse,
    ExportOutlineRequest,
    ExportOutlineResponse,
    ExtractModulesRequest,
    ExtractModulesResponse,
    GenerateOutlineRequest,
    GeneratedOutline,
    RetrieveCasesRequest,
    RetrieveCasesResponse,
    SelectModulesRequest,
    SelectModulesResponse,
    TaskInput,
    ValidateOutlineResponse,
)
from taes.services.classifier import classify_task
from taes.services.retriever import retrieve_cases
from taes.services.module_extractor import extract_module_candidates
from taes.services.ahp_selector import select_modules
from taes.services.outline_assembler import assemble_outline
from taes.services.validator import validate_outline
from taes.services.quick_evaluator import quick_extract_items, build_edges, quick_score
from taes.services.exporter import export_outline_files
from taes.services.pipeline import run_evaluation_pipeline

app = FastAPI(title="tech-achievement-eval-system", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/classify-task", response_model=ClassifiedTask)
def classify_task_api(req: TaskInput):
    return classify_task(req)


@app.post("/retrieve-cases", response_model=RetrieveCasesResponse)
def retrieve_cases_api(req: RetrieveCasesRequest):
    hits = retrieve_cases(req.industry, req.task_type, req.top_n)
    return RetrieveCasesResponse(cases=hits)


@app.post("/extract-modules", response_model=ExtractModulesResponse)
def extract_modules_api(req: ExtractModulesRequest):
    candidates = extract_module_candidates(req.case_ids, req.module_types, req.task_profile)
    return ExtractModulesResponse(candidates=candidates)


@app.post("/select-modules", response_model=SelectModulesResponse)
def select_modules_api(req: SelectModulesRequest):
    result = select_modules(req.task_profile, req.candidates, req.weights)
    return SelectModulesResponse(selected=result["selected"], explanations=result["explanations"])


@app.post("/generate-outline", response_model=GeneratedOutline)
def generate_outline_api(req: GenerateOutlineRequest):
    if not req.selected_modules:
        raise HTTPException(status_code=400, detail="selected_modules cannot be empty")

    outline = assemble_outline(req.task_id, req.title, req.selected_modules)
    return outline


@app.post("/validate-outline", response_model=ValidateOutlineResponse)
def validate_outline_api(req: GeneratedOutline):
    return validate_outline(req)


@app.post("/pipeline/run")
def run_pipeline(req: TaskInput):
    return run_evaluation_pipeline(req)


@app.post("/export-outline", response_model=ExportOutlineResponse)
def export_outline(req: ExportOutlineRequest):
    word_path, pdf_path, note = export_outline_files(req.outline, req.base_name, req.export_dir)
    return ExportOutlineResponse(word_path=word_path, pdf_path=pdf_path, note=note)


@app.post("/evaluate", response_model=EvaluateResponse)
def evaluate(req: EvaluateRequest):
    extracted = quick_extract_items(req.text)
    edges = build_edges(req.title, extracted)
    score, level, reason = quick_score(extracted)
    return EvaluateResponse(
        title=req.title,
        extracted_items=extracted,
        graph_edges=edges,
        score=score,
        level=level,
        reason=reason,
    )
