from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
import os
from urllib.parse import unquote
from img_capt_lib import lib, utils
from .renderer import ResponseFormatRenderer
from .models import Folder, Image
from .serializers import FolderSerializer, ImageSerializer


@api_view(['GET', 'POST'])
@renderer_classes([ResponseFormatRenderer])
def model_init(request):
    lib.initialize()
    return Response({"msg": "success"})


@api_view(['GET', 'POST', 'DELETE'])
@renderer_classes([ResponseFormatRenderer])
def folders_view(request):
    if request.method == 'GET':
        folders = Folder.objects.all()
        serializer = FolderSerializer(folders, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        # TODO: may raise error when parsing param
        path = unquote(request.body).split("=")[-1]
        try:
            image_captions = utils.get_caption_of_all_images(path)
            folder = Folder(path=os.path.expanduser(path))
            folder.save()
            for item in image_captions:
                img = Image(folder=folder, path=item[0], data=item[1])
                img.save()
        except FileNotFoundError:
            return Response({"msg": "Folder Not Found"}, status=status.HTTP_404_NOT_FOUND)
        except lib.ModelNotInitialized:
            return Response({"msg": "Model Not Initiated"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg": "success"})


@api_view(['GET'])
@renderer_classes([ResponseFormatRenderer])
def images_view(request):
    try:
        param = request.GET['path']
        folder = Folder.objects.get(path=param)
        images = Image.objects.filter(folder=folder)
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)
    except (KeyError, Folder.DoesNotExist) as e:
        return Response({"msg": "Folder Not Found"}, status=status.HTTP_404_NOT_FOUND)
