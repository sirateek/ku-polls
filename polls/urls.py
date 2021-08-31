from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="Index"),
    path('<int:question_id>/', views.detail, name="detail"),
<<<<<<< HEAD
    path('<int:question_id>/vote/', views.vote, name="vote"),
    path('<int:question_id>/results/', views.result, name="results")
=======
    path('<int:question_id>/vote/', views.vote, name="dote"),
    path('<int:question_id>/results/', views.result, name="desult")
>>>>>>> 7bf69614e50988aa1d8f337030bb23b0e3f4e200
]
