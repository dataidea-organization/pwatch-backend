from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BillViewSet, BillReadingViewSet, ParliamentTermViewSet, MPViewSet, DebtDataViewSet, LoanViewSet, HansardViewSet, BudgetViewSet, OrderPaperViewSet, CommitteeViewSet, HomeSummaryView

router = DefaultRouter()
router.register(r'bills', BillViewSet, basename='bill')
router.register(r'readings', BillReadingViewSet, basename='reading')
router.register(r'parliament-terms', ParliamentTermViewSet, basename='parliamentterm')
router.register(r'mps', MPViewSet, basename='mp')
router.register(r'debt', DebtDataViewSet, basename='debt')
router.register(r'loans', LoanViewSet, basename='loan')
router.register(r'hansards', HansardViewSet, basename='hansard')
router.register(r'budgets', BudgetViewSet, basename='budget')
router.register(r'order-papers', OrderPaperViewSet, basename='orderpaper')
router.register(r'committees', CommitteeViewSet, basename='committee')

urlpatterns = [
    path('home-summary/', HomeSummaryView.as_view(), name='home-summary'),
    path('', include(router.urls)),
]