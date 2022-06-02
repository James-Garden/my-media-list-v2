from django.contrib import messages


def notice(request, kind, message):
    if kind not in ["primary", "secondary", "success", "danger", "warning", "info", "light", "dark"]:
        raise ValueError(f"Alert type '{kind}' is not supported")
    else:
        alert = f'<div class="alert alert-{kind} alert-dismissible fade show" role="alert">' \
                f'{message}' \
                f'<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' \
                f'</div>'
        messages.info(request, alert)
        return alert
