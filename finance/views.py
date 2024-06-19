from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from finance.forms import AddTransactionForm
from finance.models import Budget, Category, Transaction


class AddBudget(View):
    def get(self, request):
        return render(request, 'finance/add_budget.html')

    def post(self, request):
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        Budget.objects.create(name=name, amount=amount)
        return render(request, 'finance/add_budget.html', {"success": f"Budget added successfully!"})


class MyBudgets(ListView):
    model = Budget
    template_name = 'finance/my_budgets.html'


class DeleteBudget(DeleteView):
    model = Budget
    template_name = "finance/delete_form.html"
    success_url = reverse_lazy("my_budgets")


class AddTransaction(View):
    def get(self, request):
        form = AddTransactionForm()
        return render(request, "finance/form.html", {"form": form})

    def post(self, request):
        form = AddTransactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            Transaction.objects.create(amount=amount, description=description, category=category)
            return redirect("add_transaction")
        return render(request, "finance/form.html", {"form": form})


class TransactionList(ListView):
    model = Transaction
    template_name = "finance/transaction_list.html"


class DeleteTransactionView(DeleteView):
    model = Transaction
    template_name = "finance/delete_form.html"
    success_url = reverse_lazy("transaction_list")


class AddCategoryView(CreateView):
    model = Category
    fields = "__all__"
    template_name = "finance/form.html"
    success_url = reverse_lazy("add_category")


class CategoryList(ListView):
    model = Category
    template_name = "finance/category_list.html"


class UpdateCategoryView(UpdateView):
    model = Category
    fields = "__all__"

    def get_success_url(self):
        return reverse("update_category", args=(self.get_object().pk,))


class DeleteCategoryView(PermissionRequiredMixin, DeleteView):
    permission_required = ['finance.delete_category', 'finance.add_category']

    model = Category
    template_name = "finance/delete_form.html"
    success_url = reverse_lazy("category_list")
