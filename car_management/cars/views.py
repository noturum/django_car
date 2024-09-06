from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Car, Comment
from .forms import CommentForm
from .serializers import (
    CarSerializer,
    CommentSerializer,
)


class CarListView(ListView):
    model = Car
    template_name = 'cars/index.html'
    context_object_name = 'cars'


class CarDetailView(DetailView):
    model = Car
    template_name = 'cars/car_detail.html'
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.car = self.object
            comment.author = request.user
            comment.save()
            return redirect('car_detail', pk=self.object.pk)

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class CarCreateView(LoginRequiredMixin, CreateView):
    model = Car
    fields = ['make', 'model', 'year', 'description']
    template_name = 'cars/car_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CarUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView
):
    model = Car
    fields = ['make', 'model', 'year', 'description']
    template_name = 'cars/car_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        car = self.get_object()
        return self.request.user == car.owner


class CarDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    View
):
    def get_object(self):
        return get_object_or_404(
            Car,
            pk=self.kwargs['pk']
        )

    def get(self, request, *args, **kwargs):
        car = self.get_object()
        car.delete()
        return redirect('car_list')

    def test_func(self):
        car = self.get_object()
        return self.request.user == car.owner


class APICommentListCreateView(APIView):
    """
    API endpoint for listing all comments for a car or creating a new comment.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]
    http_method_names = ['get', 'post']

    def get(self, request, id):
        car = get_object_or_404(Car, pk=id)
        if not car:
            return Response(
                {"detail": "Car not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        comments = Comment.objects.filter(car=car)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        car = Car.objects.get(pk=id)
        if not car:
            return Response(
                {"detail": "Car not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        data = request.data.copy()
        data['car'] = car.id
        serializer = CommentSerializer(data=data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class APICarsListCreateView(APIView):
    """
    API view to retrieve all cars and create a car.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]
    http_method_names = ['get', 'post']

    def get(self, request):
        car = get_object_or_404(Car, pk=id)
        serializer = CarSerializer(car, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class APICarRetrieveUpdateDestroyView(APIView):
    """
    API view to retrieve, update or delete a car.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]
    http_method_names = ['get', 'put', 'delete']

    def get(self, request, id):
        car = get_object_or_404(Car, pk=id)
        serializer = CarSerializer(car)
        return Response(serializer.data)

    def put(self, request, id):
        car = get_object_or_404(Car, pk=id)
        serializer = CarSerializer(car, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        car = get_object_or_404(Car, pk=id)
        if car.owner != request.user:
            return Response({"detail": "You are not the owner of this car."}, status=status.HTTP_403_FORBIDDEN)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
