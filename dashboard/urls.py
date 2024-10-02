from rest_framework.urls import path
from rest_framework_nested import routers
from .views import TaskViewSet, SubTaskViewSet

router = routers.DefaultRouter()
router.register("task", TaskViewSet, basename="task")

nested_router = routers.NestedDefaultRouter(router, "task", lookup="task")
nested_router.register("subtask", SubTaskViewSet, basename="task-subtask")

urlpatterns = router.urls + nested_router.urls
