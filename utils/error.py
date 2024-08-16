from django.http import JsonResponse

def handler_404(request,exception):
    message=("Path not found")
    response=JsonResponse(data={"error":message})
    response.status_code=404
    return response


def handler_500(request):
    message=("Internal server error")
    response=JsonResponse(data={"error":message})
    response.status_code=500
    return response