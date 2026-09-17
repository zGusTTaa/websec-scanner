from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Pages"])

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")


def render(request: Request, template: str, **context):
    return templates.TemplateResponse(
        request=request, name=template, context=context
    )


@router.get("/", response_class=HTMLResponse)
def page_dashboard(request: Request):
    return render(request, "index.html", page="dashboard")


@router.get("/targets", response_class=HTMLResponse)
def page_targets(request: Request):
    return render(request, "targets.html", page="targets")


@router.get("/scans", response_class=HTMLResponse)
def page_scans(request: Request):
    return render(request, "scans.html", page="scans")


@router.get("/scans/{scan_id}", response_class=HTMLResponse)
def page_scan_detail(request: Request, scan_id: int):
    return render(request, "scan_detail.html", page="scans", scan_id=scan_id)