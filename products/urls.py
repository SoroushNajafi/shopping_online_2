from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<int:category_id>/', views.ProductsByCategoryListView.as_view(), name='products_by_category'),
    path('', views.ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('comment/<int:product_id>/', views.CommentCreateView.as_view(), name='comment_create'),
]
