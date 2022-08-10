from rest_framework.response import Response
from rest_framework import views
from rest_framework import generics

from apps.products.models import Category
from apps.products.serializers import CategorySerializer

# class CategoryList(views.APIView):
#     def get(self, request):
#         queryset = Category.objects.all()
#         serializer = CategorySerializer(queryset, many=True)
#         return Response(serializer.data)


class CategoryList(generics.GenericAPIView):
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        root_nodes = Category.objects.all().get_cached_trees()

        data = []
        for n in root_nodes:
            data.append(self.recursive_node_to_dict(n))

        return Response(data)

    def recursive_node_to_dict(self, node):
        result = self.get_serializer(instance=node).data
        children = [self.recursive_node_to_dict(c) for c in node.get_children()]
        if children:
            result["children"] = children
        return result