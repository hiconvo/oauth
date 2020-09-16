from .templates import templates


async def oauth_form(request):
    context = {"request": request}
    return templates.TemplateResponse("oauth_form.html", context)


async def oauth(request):
    context = {"request": request}
    return templates.TemplateResponse("oauth_form.html", context)


async def email_form(request):
    context = {"request": request}
    return templates.TemplateResponse("email_form.html", context)


async def email(request):
    context = {"request": request}
    return templates.TemplateResponse("email_form.html", context)
