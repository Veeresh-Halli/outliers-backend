from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from todo import models as todo_models
from django.contrib.auth.models import User
from todo import serializers as todo_serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from todo.utils import is_permission_allowed

# Create your views here.


class TasksAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        all_tasks = todo_models.Task.objects.filter(user=request.user)
        task_list = [task.get_details() for task in all_tasks]
        return Response(
            status=status.HTTP_200_OK,
            data=task_list,
        )

    @staticmethod
    def post(request):
        serializer_instance = todo_serializers.TaskSerializers(data=request.data)
        if not serializer_instance.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data=serializer_instance.errors
            )

        serialized_data = serializer_instance.validated_data

        task_instance = todo_models.Task.objects.create(
            user=request.user,
            title=serialized_data.get("title"),
            description=serialized_data.get("description"),
        )
        return Response(
            status=status.HTTP_201_CREATED,
            data={
                "message": f"Task created successfully,and task_id is {task_instance.task_id}"
            },
        )


class TaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, task_id):
        try:
            task_instance = todo_models.Task.objects.get(task_id=task_id)
            if is_permission_allowed(task_instance, request.user):
                return Response(
                    status=status.HTTP_200_OK,
                    data=task_instance.get_details(),
                )
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"message": "You don't have the permission for this operation."},
            )

        except todo_models.Task.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": "Task Doesn't Exists."},
            )

    @staticmethod
    def put(request, task_id):
        serializer_instance = todo_serializers.TaskSerializers(data=request.data)

        if not serializer_instance.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data=serializer_instance.errors
            )

        serialized_data = serializer_instance.validated_data
        try:
            task_instance = todo_models.Task.objects.get(task_id=task_id)
            if is_permission_allowed(task_instance, request.user):
                task_instance.title = serialized_data.get("title")
                task_instance.description = serialized_data.get("description")
                task_instance.save()

                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        "message": f"Task successfully updates for task_id {task_id}"
                    },
                )
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"message": "You don't have the permission for this operation."},
            )

        except todo_models.Task.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": "Task Doesn't Exists."},
            )

    @staticmethod
    def delete(request, task_id):
        try:
            task_instance = todo_models.Task.objects.get(task_id=task_id)
            if is_permission_allowed(task_instance, request.user):
                task_instance.delete()

                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        "message": f"Task successfully deleted for task_id {task_id}"
                    },
                )
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"message": "You don't have the permission for this operation."},
            )
        except todo_models.Task.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": "Task Doesn't Exists."},
            )


class ToggleTaskAPIView(APIView):
    @staticmethod
    def post(request, task_id):
        serializer_instance = todo_serializers.ToggleTaskSerializer(data=request.data)

        if not serializer_instance.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data=serializer_instance.errors
            )
        serialized_data = serializer_instance.validated_data
        try:
            task_instance = todo_models.Task.objects.get(task_id=task_id)
            if is_permission_allowed(task_instance, request.user):
                task_instance.completed = serialized_data.get("completed")
                task_instance.save()

                return Response(
                    status=status.HTTP_200_OK,
                    data={"message": f"Toggled successfully for task_id {task_id}"},
                )
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"message": "You don't have the permission for this operation."},
            )
        except todo_models.Task.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": "Task Doesn't Exists."},
            )
