from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append(
    {
        "id": str(uuid.uuid4()),
        "name": "User01",
        "email": "user01@example.com",
        "is_active": True,
    }
)
data_list.append(
    {
        "id": str(uuid.uuid4()),
        "name": "User02",
        "email": "user02@example.com",
        "is_active": True,
    }
)
data_list.append(
    {
        "id": str(uuid.uuid4()),
        "name": "User03",
        "email": "user03@example.com",
        "is_active": False,
    }
)  # Ejemplo de item inactivo


class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):
        """
        Retorna solo los datos con is_active=True como JSON con status 200 OK
        """
        active_data = [item for item in data_list if item.get("is_active") == True]
        return Response(active_data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Crea un nuevo elemento en data_list
        """
        # Extraer los datos enviados en el cuerpo de la solicitud
        data = request.data

        # Validar que los campos name y email estén presentes
        if "name" not in data or "email" not in data:
            return Response(
                {"error": "Los campos 'name' y 'email' son requeridos"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validar que los campos no estén vacíos
        if not data.get("name") or not data.get("email"):
            return Response(
                {"error": "Los campos 'name' y 'email' no pueden estar vacíos"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Si los campos son válidos:
        data["id"] = str(uuid.uuid4())
        data["is_active"] = True
        data_list.append(data)

        # Retornar respuesta con código 201, mensaje de éxito y datos guardados
        return Response(
            {"message": "Usuario creado exitosamente", "data": data},
            status=status.HTTP_201_CREATED,
        )


class DemoRestApiItem(APIView):
    name = "Demo REST API Item"

    def get_item_by_id(self, item_id):
        """
        Función auxiliar para encontrar un elemento por ID
        """
        for item in data_list:
            if item.get("id") == item_id:
                return item
        return None

    def get(self, request, item_id):
        """
        FUNCIÓN DE PRUEBA

        Retorna solo los datos con is_active=True como JSON con status 200 OK
        """
        active_data = [item for item in data_list if item.get("is_active") == True]
        return Response(active_data, status=status.HTTP_200_OK)

    def put(self, request, item_id):
        """
        PUT: Reemplaza completamente los datos de un elemento del arreglo,
        excepto el identificador que se envía como campo obligatorio en el cuerpo de la solicitud.
        """
        data = request.data

        # Validar que los campos name y email estén presentes
        if "name" not in data or "email" not in data:
            return Response(
                {"error": "Los campos 'name' y 'email' son requeridos"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validar que los campos no estén vacíos
        if not data.get("name") or not data.get("email"):
            return Response(
                {"error": "Los campos 'name' y 'email' no pueden estar vacíos"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Buscar el elemento a actualizar
        item = self.get_item_by_id(item_id)
        if not item:
            return Response(
                {"error": "Elemento no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        # Reemplazar completamente los datos, manteniendo el ID
        item["name"] = data["name"]
        item["email"] = data["email"]
        item["is_active"] = data.get(
            "is_active", True
        )  # Si no se envía, mantiene True por defecto

        return Response(
            {"message": "Elemento actualizado completamente", "data": item},
            status=status.HTTP_200_OK,
        )

    def patch(self, request, item_id):
        """
        PATCH: Actualiza parcialmente los campos del elemento identificado por su identificador,
        manteniendo los valores no modificados.
        """
        data = request.data

        # Buscar el elemento a actualizar
        item = self.get_item_by_id(item_id)
        if not item:
            return Response(
                {"error": "Elemento no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        # Actualizar solo los campos enviados
        if "name" in data:
            if not data["name"]:  # Validar que no esté vacío si se envía
                return Response(
                    {"error": "El campo 'name' no puede estar vacío"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            item["name"] = data["name"]

        if "email" in data:
            if not data["email"]:  # Validar que no esté vacío si se envía
                return Response(
                    {"error": "El campo 'email' no puede estar vacío"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            item["email"] = data["email"]

        if "is_active" in data:
            item["is_active"] = data["is_active"]

        return Response(
            {"message": "Elemento actualizado parcialmente", "data": item},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, item_id):
        """
        DELETE: Elimina lógicamente un elemento del arreglo según el identificador proporcionado.
        """
        # Buscar el elemento a eliminar
        item = self.get_item_by_id(item_id)
        if not item:
            return Response(
                {"error": "Elemento no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        # Eliminación lógica: cambiar is_active a False
        item["is_active"] = False

        return Response(
            {"message": "Elemento eliminado lógicamente", "data": item},
            status=status.HTTP_200_OK,
        )
