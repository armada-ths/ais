from django.shortcuts import render, redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.contrib.auth.models import User

from fair.models import Fair
from recruitment.models import RecruitmentApplication, RecruitmentPeriod

from .models import Profile
from .forms import ProfileForm


def list_people(request, year):
    fair = get_object_or_404(Fair, year=year)

    recruitment_applications = list(
        RecruitmentApplication.objects.filter(
            recruitment_period__fair=fair,
            status="accepted",
        )
        .prefetch_related(
            "user",
            "delegated_role",
            "recruitment_period",
            "delegated_role__organization_group",
        )
        .order_by(
            "delegated_role__organizationgroup",
            "recruitment_period__startdate",
            "delegated_role",
            "user__first_name",
            "user__last_name",
        )
    )

    groups = {
        group
        for group in [
            application.delegated_role.organization_group
            for application in recruitment_applications
        ]
    }

    organization_groups = [
        {
            "i": i,
            "name": group.name,
            "users": [
                recruitment_application
                for recruitment_application in recruitment_applications
                if group == recruitment_application.delegated_role.organization_group
            ],
        }
        for i, group in enumerate(groups)
    ]

    total = len(recruitment_applications)

    return render(
        request,
        "people/list.html",
        {
            "fair": fair,
            "organization_groups": organization_groups,
            "total": total,
            "recruitment_periods": RecruitmentPeriod.objects.filter(fair=fair),
        },
    )


def profile(request, year, pk):
    fair = get_object_or_404(Fair, year=year)
    user = get_object_or_404(User, pk=pk)

    profile = Profile.objects.filter(user=user).first()

    if not profile:
        profile = Profile.objects.create(user=user, no_dietary_restrictions=False)

    application = RecruitmentApplication.objects.filter(
        user=user, status="accepted", recruitment_period__fair=fair
    ).first()

    return TemplateResponse(
        request,
        "people/profile.html",
        {
            "fair": fair,
            "profile": profile,
            "role": application.delegated_role if application else None,
            "roles": RecruitmentApplication.objects.filter(
                user=user, status="accepted"
            ).order_by("recruitment_period__fair"),
        },
    )


def profile_delete(request, year, pk):
    fair = get_object_or_404(Fair, year=year)
    user = request.session["user"]

    if request.method == "POST":
        Profile.objects.filter(user=request.user).delete()
        User.objects.filter(pk=pk).delete()
        return redirect("/accounts/logout?next=/")

    profile = Profile.objects.filter(user=user).first()

    return TemplateResponse(
        request,
        "people/profile.html",
        {
            "fair": fair,
            "profile": profile,
            "roles": RecruitmentApplication.objects.filter(
                user=user, status="accepted"
            ).order_by("recruitment_period__fair"),
        },
    )


def edit(request, year):
    fair = get_object_or_404(Fair, year=year)

    profile = Profile.objects.filter(user=request.user).first()

    if not profile:
        profile = Profile.objects.create(user=request.user)

    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)

    if form.is_valid():
        form.save()
        return redirect("people:profile", fair.year, request.user.pk)

    application = RecruitmentApplication.objects.filter(
        recruitment_period__fair=fair, user=request.user, status="accepted"
    ).first()

    return TemplateResponse(
        request,
        "people/edit.html",
        {
            "fair": fair,
            "profile": profile,
            "role": application.delegated_role if application else None,
            "form": form,
        },
    )
