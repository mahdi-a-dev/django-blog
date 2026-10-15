from django.contrib.auth.views import (
    LogoutView,
    PasswordChangeDoneView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # user authentication
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    
    # users profile
    path("profile/", views.ProfilePage.as_view(), name="profile"),
    path("profile/edit", views.EditProfile.as_view(), name="edit-profile"),
    
    # change password
    path("password/change/", views.ChangePassword.as_view(), name="password-change"),
    path("password/change/done/", views.ChangePasswordDone.as_view(), name="password-change-done"),
    
    # reset password
    # path("password/reset/", views.ResetPassword.as_view(), name="password-reset"),
    
    # path("password/reset/done/", PasswordResetDoneView.as_view(
    #     template_name = "accounts/password_reset-done.html"
    # ), name="password-reset-done"),

]
