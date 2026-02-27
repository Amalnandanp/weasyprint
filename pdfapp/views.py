from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from django.shortcuts import render
from django.conf import settings
from weasyprint import HTML, CSS
import os

def home(request):
    # Get all HTML templates from payslip folder
    payslip_dir = os.path.join(settings.BASE_DIR, "templates/payslip")
    templates = sorted([f for f in os.listdir(payslip_dir) if f.endswith('.html')])

    context = {'templates': templates}
    return render(request, "home.html", context)

def generate_pdf(request, template_name):
    # Validate template name to prevent directory traversal
    if ".." in template_name or template_name.startswith('/'):
        raise Http404("Invalid template name")

    template_path = f"payslip/{template_name}"
    payslip_file = os.path.join(settings.BASE_DIR, "templates", template_path)

    # Check if file exists and is in payslip folder
    if not os.path.exists(payslip_file):
        raise Http404("Template not found")

    html_string = render_to_string(template_path)

    css_common = os.path.join(settings.BASE_DIR, "static/css/common.css")
    css_utility = os.path.join(settings.BASE_DIR, "static/css/style.css")

    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri('/')
    ).write_pdf(
        stylesheets=[CSS(css_common), CSS(css_utility)]
    )

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f"inline; filename={template_name.replace('.html', '.pdf')}"
    return response