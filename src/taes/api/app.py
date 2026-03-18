from fastapi import FastAPI
from taes.schemas import EvalRequest, EvalResponse
from taes.extract.rules import extract_items
from taes.graph.builder import build_edges
from taes.scoring.ahp import score_items

app = FastAPI(title="tech-achievement-eval-system", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/evaluate", response_model=EvalResponse)
def evaluate(req: EvalRequest):
    extracted = extract_items(req.text)
    edges = build_edges(req.title, extracted)
    score, level, reason = score_items(extracted)

    return EvalResponse(
        title=req.title,
        extracted_items=extracted,
        graph_edges=edges,
        score=score,
        level=level,
        reason=reason,
    )
