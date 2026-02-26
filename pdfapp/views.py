from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from django.shortcuts import render
from django.conf import settings
from weasyprint import HTML, CSS
import os


def home(request):
    return render(request, "home.html")


def generate_pdf(request, template_id):

    template_map = {
        "1": "payslip/templete1.html",
        "2": "payslip/templete2.html",
    }

    template_name = template_map.get(template_id)

    if not template_name:
        raise Http404("Template not found")

    html_string = render_to_string(template_name)

    # Absolute path to shared CSS
    css_common = os.path.join(settings.BASE_DIR, "static/css/common.css")
    css_utility = os.path.join(settings.BASE_DIR, "static/css/style.css")

    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri('/')
    ).write_pdf(
        stylesheets=[CSS(css_common), CSS(css_utility)]
    )

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f"inline; filename=template_{template_id}.pdf"
    return response