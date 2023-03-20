import json
from pathlib import Path

from django import forms
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView

from hw.jana_sergienko.lesson04.lecture import task_01_money
from hw.jana_sergienko.lesson04.lecture import task_02_sign
from hw.jana_sergienko.lesson04.lecture import task_03_triangle
from hw.jana_sergienko.lesson04.lecture import task_04_palindrom


def helloworld(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello from app")


def handle_task_01_money(request: HttpRequest) -> HttpResponse:
    if not request.POST:
        return render(request, "app_jana_sergienko/task01.html")

    rub = int(request.POST["r"])
    coin = int(request.POST["c"])
    amt = int(request.POST["a"])
    result = task_01_money(rub, coin, amt)

    payload = {
        "data": {
            "rubles": rub,
            "coins": coin,
            "amount": amt,
            "result": float(result),
        }
    }

    return JsonResponse(payload)


def handle_task_02_sign(request: HttpRequest) -> HttpResponse:
    if not request.POST:
        return render(request, "app_jana_sergienko/task02.html")

    number = float(request.POST["n"])
    result = task_02_sign(number)

    payload = {
        "data": {
            "number": number,
            "result": result,
        }
    }

    return JsonResponse(payload)


def handle_task_03_triangle(request: HttpRequest) -> HttpResponse:
    if not request.POST:
        return render(request, "app_jana_sergienko/task03.html")

    side1 = int(request.POST["s1"])
    side2 = int(request.POST["s2"])
    side3 = int(request.POST["s3"])
    result = task_03_triangle(side1, side2, side3)

    payload = {
        "data": {
            "side1": side1,
            "side2": side2,
            "side3": side3,
            "result": result,
        }
    }

    return JsonResponse(payload)


def handle_task_04_palindrom(request: HttpRequest) -> HttpResponse:
    if not request.POST:
        return render(request, "app_jana_sergienko/task04.html")

    str_ = request.POST["str"]
    result = task_04_palindrom(str_)

    payload = {
        "data": {
            "line": str_,
            "result": result,
        }
    }

    return JsonResponse(payload)


def save_number(num: int) -> None:
    dir_repo = Path(__file__).parent.parent
    dir_artifacts = dir_repo / ".artifacts"
    file_path = dir_artifacts / "jana_sergienko.json"

    try:
        with file_path.open("r") as stream:
            numbers = json.load(stream)
    except (OSError, json.JSONDecodeError):
        numbers = []

    numbers.append(num)

    with file_path.open("w") as stream:
        json.dump(numbers, stream)


def calc_avg() -> float:
    dir_repo = Path(__file__).parent.parent
    dir_artifacts = dir_repo / ".artifacts"
    file_path = dir_artifacts / "jana_sergienko.json"

    try:
        with file_path.open("r") as stream:
            numbers = json.load(stream)
    except (OSError, json.JSONDecodeError):
        numbers = []

    if not numbers:
        return 0

    return float(sum(numbers)) / len(numbers)


def handle_average(request: HttpRequest) -> HttpResponse:
    if request.POST:
        number = int(request.POST["number"])
        save_number(number)
    number_avg = calc_avg()
    context = {"number_avg": number_avg}
    return render(request, "app_jana_sergienko/average.html", context)


class AverageView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return self.render_template()

    def post(self, request: HttpRequest) -> HttpResponse:
        number = int(request.POST["number"])
        save_number(number)

        return self.render_template()

    def render_template(self) -> HttpResponse:
        number_avg = calc_avg()
        context = {"number_avg": number_avg}

        return render(
            self.request,
            "app_jana_sergienko/classAverage.html",
            context,
        )


class AverageForm(forms.Form):
    number = forms.IntegerField(label="Enter number:")


@method_decorator(csrf_exempt, name="dispatch")
class AverView(FormView):
    form_class = AverageForm
    success_url = "/~/jana_sergienko/avgForm/"
    template_name = "app_jana_sergienko/avgForm.html"

    def form_valid(self, form: forms.Form) -> HttpResponse:
        number = form.cleaned_data["number"]
        save_number(number)
        return super().form_valid(form)

    def get_context_data(self, **kwargs: dict) -> dict:
        ctx = super().get_context_data()
        return ctx | {
            "number_avg": calc_avg(),
        }
