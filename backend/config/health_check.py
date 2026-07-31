from django.db import connection
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET


@require_GET
@never_cache
def health_check(request):
    """Liveness + DB connectivity check for container orchestration."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception as exc:
        return JsonResponse(
            {"status": "error", "database": "unreachable", "detail": str(exc)},
            status=503,
        )

    return JsonResponse({"status": "ok", "database": "ok"})