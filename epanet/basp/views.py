from . import models
from rest_framework import viewsets
from rest_framework.parsers import FileUploadParser
from django.db import connection
from . import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from . import watersim
from . import dbcommunication
from . import databaseTables
from datetime import datetime
import basp.dbcommunication as dbcommunication
import datetime as dtmsavewaterdata
from django.shortcuts import get_object_or_404
import ast
import math
from random import choices
import json
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
import os
import shutil
import re
from django.core.files.base import ContentFile
from drf_yasg.utils import swagger_auto_schema
from django.http import FileResponse
from drf_yasg import openapi
from . import sensorsProfile
import traci
from influxdb import InfluxDBClient
import wntr
import yaml
import paramiko
from scp import SCPClient
import time
from . import addleakages

#UPDATED
class WaterView(viewsets.ViewSet):
    """Water View"""
    @swagger_auto_schema(responses={200: openapi.Response('ok, data returned')})
    def list(self, request):
        """This endpoint returns a list of all the editable EPANET input file fields"""
        editable_fields = [
            'Backdrop',
            'Coordinates',
            'Vertices',
            'Labels',
            'Options',
            'Times',
            'Report',
            'Quality',
            'Reactions',
            'Sources',
            'Mixing',
            'Curves',
            'Patterns',
            'Energy',
            'Status',
            'Controls',
            'Rules',
            'Demands',
            'Title',
            'Junctions',
            'Reservoirs',
            'Tanks',
            'Pipes',
            'Pumps',
            'Valves',
            'Emitters'
        ]
        return Response(status=status.HTTP_200_OK,data={'Title': 'KIOS BaSP REST API for Water Simulations', 'information': 'Here you can read/edit the EPANET inp file, the fields you can edit are listed in details', 'details': editable_fields})


#UPDATED
class WaterDeleteDBViewSet(viewsets.ViewSet):
    """
        Information
        Use this API endpoint to delete existing experiments from database.
        Provide the experiments names in a list.
    """
    serializer_class = serializers.WaterDeleteDBViewSet

    @swagger_auto_schema(responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def list(self, request):
        """Returns a list of all the experiments available for deleting"""
        try:
            existing_ex_names = list(models.ExperimentNames.objects.all())
            allthenames = []
            for value in existing_ex_names:
                allthenames.append(value.ex_name)
            return Response(status=status.HTTP_200_OK,data={'Title': 'KIOS BaSP REST API for Water Simulations',
                             'information': 'Here you can delete experiments from BaSP',
                             'experiments': allthenames})
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def post(self, request):
        """Use this endpoint to delete experiments"""
        import shutil
        import basp.dbcommunication as dbcommunication
        existing_ex_names = list(models.ExperimentNames.objects.all())
        allthenames = []
        for value in existing_ex_names:
            allthenames.append(value.ex_name)
        serializer = serializers.WaterDeleteDBViewSet(data=request.data)
        if serializer.is_valid():
            experimentname = serializer.data.get('experimentname')
            if experimentname is not None:
                if "[" not in experimentname or "]" not in experimentname:
                    return Response(status=status.HTTP_400_BAD_REQUEST,data={'message':'experimentname must be a list','allowed experiment names': allthenames})
                else:
                    try:
                        client = InfluxDBClient(host='influxdb', port=8086, username='kios',password='kios1234!', database='virtual_city')
                    except:
                        client.close()
                    try:
                        newlinks = ast.literal_eval(experimentname)
                        newlinks = [str(n).strip() for n in newlinks]
                        for value in newlinks:
                            scada = 'water_output_'+value+'_scada_sensors'
                            sensors = 'water_output_'+value+'_sensors'
                            # postgresql_query = 'DROP TABLE IF EXISTS '+scada
                            client.drop_measurement(scada)
                            client.drop_measurement(sensors)
                            models.ExperimentNames.objects.filter(ex_name=value).delete()
                            dir_path  = "basp\\uploads\\" + str(value)
                            try:
                                shutil.rmtree(dir_path)
                            except:
                                x='no folder'
                            # dbcommunication.db_tables_simple_query(postgresql_query)
                        existing_ex_names = list(models.ExperimentNames.objects.all())
                        allthenames = []
                        for value in existing_ex_names:
                            allthenames.append(value.ex_name)
                        return Response(status=status.HTTP_200_OK,data={'message': 'Data Deleted'})
                    except:
                        return Response(status=status.HTTP_400_BAD_REQUEST,data={'message': 'invalid experiment name/s','allowed experiment names': allthenames})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST,data={'message': 'invalid experiment name/s','allowed experiment names': allthenames})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#UPDATED, REMOVED Create (not needed)
class WaterBackdropViewSet(viewsets.ViewSet):
    """
        Information
        Use this API endpoint to read, and update Backdrop.
    """
    serializer_class = serializers.WaterBackdropSerializer

    @swagger_auto_schema(responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def list(self, request):
        """Use this endpoint to read all the backdrop data from the database"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            return Response(status=status.HTTP_200_OK, data={'DIMENSIONS': wn.options.graphics.dimensions,'UNITS':wn.options.graphics.units,
                                                             'FILE':wn.options.graphics.image_filename,'OFFSET':wn.options.graphics.offset})
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def retrieve(self, request, pk=None):
        """Use this endpoint to read a specific backdrop entry using its id"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            if pk == 'DIMENSIONS':
                data = {pk: wn.options.graphics.dimensions}
            elif pk == 'UNITS':
                data = {pk: wn.options.graphics.units}
            elif pk == 'FILE':
                data = {pk: wn.options.graphics.image_filename}
            elif pk == 'OFFSET':
                data = {pk: wn.options.graphics.offset}
            return Response(status=status.HTTP_200_OK,data=data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: openapi.Response('ok, entry deleted'), 400: openapi.Response('error, bad request')})
    def destroy(self, request, pk=None):
        """Use this endpoint to remove a backdrop from the database using its id"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            if pk == 'DIMENSIONS':
                wn.options.graphics.dimensions=None
                wn.write_inpfile(inp_file)
                return Response(status=status.HTTP_200_OK)
            elif pk == 'UNITS':
                wn.options.graphics.units=None
                wn.write_inpfile(inp_file)
                return Response(status=status.HTTP_200_OK)
            elif pk == 'FILE':
                wn.options.graphics.image_filename=None
                wn.write_inpfile(inp_file)
                return Response(status=status.HTTP_200_OK)
            elif pk == 'OFFSET':
                wn.options.graphics.offset=None
                wn.write_inpfile(inp_file)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: openapi.Response('ok, entry updated'), 400: openapi.Response('error, bad request')})
    def update(self, request, pk=None):
        """Use this endpoint to update a backdrop using its id"""
        serializer = serializers.WaterBackdropSerializer(data=request.data)
        if serializer.is_valid():
            try:
                inp_file = 'basp/Water/Water.inp'
                wn = wntr.network.WaterNetworkModel(inp_file)
                if pk == 'DIMENSIONS':
                    wn.options.graphics.dimensions = json.loads(serializer.data.get('value'))
                    wn.write_inpfile(inp_file)
                    return Response(status=status.HTTP_200_OK)
                elif pk == 'UNITS':
                    wn.options.graphics.units = serializer.data.get('value')
                    wn.write_inpfile(inp_file)
                    return Response(status=status.HTTP_200_OK)
                elif pk == 'FILE':
                    wn.options.graphics.image_filename = serializer.data.get('value')
                    wn.write_inpfile(inp_file)
                    return Response(status=status.HTTP_200_OK)
                elif pk == 'OFFSET':
                    wn.options.graphics.offset = json.loads(serializer.data.get('value'))
                    wn.write_inpfile(inp_file)
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#UPDATED
class WaterControlsViewSet(viewsets.ViewSet):
    """
        Information
        Use this API endpoint to read, create and update Controls.
    """
    serializer_class = serializers.WaterControlsSerializer

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def list(self, request):
        """Use this endpoint to read all the control data from the database"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            return Response(status=status.HTTP_200_OK,data={'controls': wn.control_name_list})
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def retrieve(self, request, pk=None):
        """Use this endpoint to read a specific control entry using its id"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            data = {'name':pk,'actions':str(),'condition':str(wn.get_control(pk).condition)}
            return Response(status=status.HTTP_200_OK, data=data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, entry created'), 400: openapi.Response('error, bad request')})
    def create(self, request):
        """Use this endpoint to add a control to the database"""
        serializer = serializers.WaterBackdropSerializer(data=request.data)
        if serializer.is_valid():
            try:
                inp_file = 'basp/Water/Water.inp'
                wn = wntr.network.WaterNetworkModel(inp_file)
                wn.add_control(serializer.data.get('name'))
                wn.get_control(serializer.data.get('name')).actions()[0]=serializer.data.get('actions')
                wn.get_control(serializer.data.get('name')).condition = serializer.data.get('condition')
                wn.write_inpfile(inp_file)
                return Response(status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: openapi.Response('ok, entry updated'), 400: openapi.Response('error, bad request'), 404: openapi.Response('error, entry not found')})
    def update(self, request, pk=None):
        """Use this endpoint to update a control using its id"""
        serializer = serializers.WaterControlsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                inp_file = 'basp/Water/Water.inp'
                wn = wntr.network.WaterNetworkModel(inp_file)
                wn.get_control(serializer.data.get(pk)).actions()[0] = serializer.data.get('actions')
                wn.get_control(serializer.data.get(pk)).condition = serializer.data.get('condition')
                wn.write_inpfile(inp_file)
                return Response(status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, entry deleted'), 404: openapi.Response('error, entry not found')})
    def destroy(self, request, pk=None):
        """Use this endpoint to remove a control from the database using its id"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            wn.remove_control(pk)
            wn.write_inpfile(inp_file)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


#UPDATED
class WaterCoordinatesViewSet(viewsets.ViewSet):
    """
        Information
        Use this API endpoint to read, create and update Coordinates.
    """
    serializer_class = serializers.WaterCoordinatesSerializer

    @swagger_auto_schema(responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def list(self, request):
        """Use this endpoint to read all the coordinates data from the database"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            allnodes = wn.node_name_list
            finalcoordinates = []
            for value in allnodes:
                node = wn.get_node(value)
                coord = {'node':value,'X-Coord':node.coordinates[0],'Y-Coord':node.coordinates[1]}
                finalcoordinates.append(coord)
            return Response(status=status.HTTP_200_OK, data={'coordinates': finalcoordinates})
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: openapi.Response('ok, data returned'), 404: openapi.Response('error, entry not found')})
    def retrieve(self, request, pk=None):
        """Use this endpoint to read a specific coordinate entry using its id"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            allnodes = wn.node_name_list
            node = wn.get_node(pk)
            coord = {'node': pk, 'X-Coord': node.coordinates[0], 'Y-Coord': node.coordinates[1]}
            return Response(status=status.HTTP_200_OK, data={'coordinates': coord})
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(responses={200: openapi.Response('ok, entry updated'), 400: openapi.Response('error, bad request')})
    def update(self, request, pk=None):
        """Use this endpoint to update a coordinate using its id"""
        serializer = serializers.WaterCoordinatesSerializer(data=request.data)
        if serializer.is_valid():
            try:
                inp_file = 'basp/Water/Water.inp'
                wn = wntr.network.WaterNetworkModel(inp_file)
                node = wn.get_node(pk)
                node.coordinates = (float(serializer.data.get('xcoord')), float(serializer.data.get('ycoord')))
                wn.write_inpfile(inp_file)
                return Response(status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: openapi.Response('ok, entry deleted'), 400: openapi.Response('error, bad request')})
    def destroy(self, request, pk=None):
        """Use this endpoint to remove a coordinate from the database using its id"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            node = wn.get_node(pk)
            node.coordinates = (0,0)
            wn.write_inpfile(inp_file)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


#UPDATED removed create, create & update
class WaterCurvesViewSet(viewsets.ViewSet):
    """
        Information
        Use this API endpoint to read, create and update Curves.
    """
    serializer_class = serializers.WaterCurvesSerializer

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def list(self, request):
        """Use this endpoint to read all the curves data from the database"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            allcurves = wn.curve_name_list
            finalcurves = []
            for value in allcurves:
                node = wn.get_curve(value)
                curv = {'curve':value,'curve_type':node.curve_type,'points':node.points}
                finalcurves.append(curv)
            return Response(status=status.HTTP_200_OK, data={'curves': finalcurves})
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 404: openapi.Response('error, entry not found')})
    def retrieve(self, request, pk=None):
        """Use this endpoint to read a specific curve entry using its id"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            node = wn.get_curve(pk)
            curv = {'curve': pk, 'curve_type': node.curve_type, 'points': node.points}
            return Response(status=status.HTTP_200_OK, data={'curves': curv})
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


#UPDATED, REMOVED Create (not needed)
class WaterEmittersViewSet(viewsets.ViewSet):
    """
        Information
        Use this API endpoint to read, create and update Emitters.
    """
    serializer_class = serializers.WaterEmittersSerializer
    @swagger_auto_schema(responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def list(self, request):
        """Use this endpoint to read all the emitters data from the database"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            allnodes = wn.node_name_list
            finalemit = []
            for value in allnodes:
                try:
                    node = wn.get_node(value)
                    emit = {'node': value, 'Flow coefficient': node.emitter_coefficient}
                    finalemit.append(emit)
                except:
                    msg='no emitter'
            return Response(status=status.HTTP_200_OK, data={'emitters': finalemit})
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def retrieve(self, request, pk=None):
        """Use this endpoint to read a specific emitter entry using its id"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            node = wn.get_node(pk)
            emit = {'node': pk, 'Flow coefficient': node.emitter_coefficient}
            return Response(status=status.HTTP_200_OK, data=emit)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: openapi.Response('ok, entry updated'), 400: openapi.Response('error, bad request')})
    def update(self, request, pk=None):
        """Use this endpoint to update an emitter using its id"""
        serializer = serializers.WaterEmittersSerializer(data=request.data)
        if serializer.is_valid():
            try:
                inp_file = 'basp/Water/Water.inp'
                wn = wntr.network.WaterNetworkModel(inp_file)
                node = wn.get_node(pk)
                node.emitter_coefficient = float(serializer.data.get('flow_coefficient'))
                wn.write_inpfile(inp_file)
                return Response(status=status.HTTP_200_OK,)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: openapi.Response('ok, entry updated'), 400: openapi.Response('error, bad request')})
    def destroy(self, request, pk=None):
        """Use this endpoint to remove an emitter from the database using its id"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            node = wn.get_node(pk)
            node.emitter_coefficient = float()
            wn.write_inpfile(inp_file)
            return Response(status=status.HTTP_200_OK,)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


#UPDATED, removed create
class WaterEnergyViewSet(viewsets.ViewSet):
    """
        Information
        Use this API endpoint to read, create and update Energy.
    """
    serializer_class = serializers.WaterEnergySerializer

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def list(self, request):
        """Use this endpoint to read all the energy data from the database"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            ene = {'global_price':wn.options.energy.global_price,'global_pattern':wn.options.energy.global_pattern,
                   'global_efficiency':wn.options.energy.global_efficiency,'demand_charge':wn.options.energy.demand_charge}
            return Response(status=status.HTTP_200_OK, data={'energy': ene})
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 404: openapi.Response('error, entry not found')})
    def retrieve(self, request, pk=None):
        """Use this endpoint to read a specific energy entry using its id"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            if pk == 'global_price':
                return Response(status=status.HTTP_200_OK, data={'global_price': wn.options.energy.global_price})
            elif pk == 'global_pattern':
                return Response(status=status.HTTP_200_OK, data={'global_pattern': wn.options.energy.global_pattern})
            elif pk == 'global_efficiency':
                return Response(status=status.HTTP_200_OK, data={'global_efficiency': wn.options.energy.global_efficiency})
            elif pk == 'demand_charge':
                return Response(status=status.HTTP_200_OK, data={'demand_charge': wn.options.energy.demand_charge})
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, entry updated'), 404: openapi.Response('error, entry not found')})
    def update(self, request, pk=None):
        """Use this endpoint to update an energy using its id"""
        serializer = serializers.WaterEnergySerializer(data=request.data)
        if serializer.is_valid():
            try:
                inp_file = 'basp/Water/Water.inp'
                wn = wntr.network.WaterNetworkModel(inp_file)
                if pk == 'global_price':
                    wn.options.energy.global_price = float(serializer.data.get('value'))
                    wn.write_inpfile(inp_file)
                    return Response(status=status.HTTP_200_OK)
                elif pk == 'global_pattern':
                    wn.options.energy.global_pattern = str(serializer.data.get('value'))
                    wn.write_inpfile(inp_file)
                    return Response(status=status.HTTP_200_OK)
                elif pk == 'global_efficiency':
                    wn.options.energy.global_efficiency = float(serializer.data.get('value'))
                    wn.write_inpfile(inp_file)
                    return Response(status=status.HTTP_200_OK)
                elif pk == 'demand_charge':
                    wn.options.energy.demand_charge = float(serializer.data.get('value'))
                    wn.write_inpfile(inp_file)
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, entry created'), 400: openapi.Response('error, bad request')})
    def destroy(self, request, pk=None):
        """Use this endpoint to remove an energy from the database using its id"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            if pk == 'global_price':
                wn.options.energy.global_price = float(0.0)
                wn.write_inpfile(inp_file)
                return Response(status=status.HTTP_200_OK)
            elif pk == 'global_pattern':
                wn.options.energy.global_pattern = None
                wn.write_inpfile(inp_file)
                return Response(status=status.HTTP_200_OK)
            elif pk == 'global_efficiency':
                wn.options.energy.global_efficiency = float(0.0)
                wn.write_inpfile(inp_file)
                return Response(status=status.HTTP_200_OK)
            elif pk == 'demand_charge':
                wn.options.energy.demand_charge = float(0.0)
                wn.write_inpfile(inp_file)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


#UPDATED, REMOVED destroy, create and update
class WaterJunctionsViewSet(viewsets.ViewSet):
    """
        Information
        Use this API endpoint to read, create and update Junctions.
    """
    serializer_class = serializers.WaterJunctionsSerializer
    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def list(self, request):
        """Use this endpoint to read all the junction data from the database"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            return Response(status=status.HTTP_200_OK, data=wn.junction_name_list)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 404: openapi.Response('error, entry not found')})
    def retrieve(self, request, pk=None):
        """Use this endpoint to read a specific junction entry using its id"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            if pk in wn.junction_name_list:
                junction = wn.nodes[pk]
                base_demands = junction.demand_timeseries_list.base_demand_list()
                demand_patterns = junction.demand_timeseries_list.pattern_list()
                if base_demands:
                    base_demand = base_demands[0]
                else:
                    base_demand = 0.0
                if demand_patterns:
                    if demand_patterns[0] == wn.options.hydraulic.pattern:
                        demand_pattern = None
                    else:
                        demand_pattern = demand_patterns[0]
                else:
                    demand_pattern = None
                data = {'junction':pk,'elevation':junction.elevation,'demand':str(base_demand),'pattern':str(demand_pattern)}
                return Response(status=status.HTTP_200_OK,data=data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


#UPDATED, REMOVED retrieve,create,update,destroy (not needed)
class WaterLabelsViewSet(viewsets.ViewSet):
    """
        Information
        Use this API endpoint to read, create and update Labels.
    """
    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def list(self, request):
        """Use this endpoint to read all the labels data from the database"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            return Response(status=status.HTTP_200_OK,data=wn._labels)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


#UPDATED, REMOVED create, update, destroy
class WaterMixingViewSet(viewsets.ViewSet):
    """
        Information
        Use this API endpoint to read, create and update Mixing.
    """
    serializer_class = serializers.WaterMixingSerializer

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def list(self, request):
        """Use this endpoint to read all the mixing data from the database"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            tanks = wn.tank_name_list
            data = []
            for value in tanks:
                data.append({'tank id':value,'Model':wn.get_node(value).mixing_model,'Fraction':wn.get_node(value).mixing_fraction})
            return Response(status=status.HTTP_200_OK, data=data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 404: openapi.Response('error, entry not found')})
    def retrieve(self, request, pk=None):
        """Use this endpoint to read a specific mixing entry using its id"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            data={'tank id': pk, 'Model': wn.get_node(pk).mixing_model,'Fraction': wn.get_node(pk).mixing_fraction}
            return Response(status=status.HTTP_200_OK, data=data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


#UPDATED, REMOVED create, update, destroy
class WaterOptionsViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to read, create and update Options.
    """
    serializer_class = serializers.WaterOptionsSerializer

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def list(self, request):
        """Use this endpoint to read all the options data from the database"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            op = wn.options
            data = {'UNITS':op.hydraulic.inpfile_units,'HEADLOSS':op.hydraulic.headloss,
                    'HYDRAULICS':op.hydraulic.hydraulics,'HYDRAULICS_FILENAME':op.hydraulic.hydraulics_filename,
                    'QUALITY_PARAMETER':op.quality.parameter,'QUALITY_TRACE_NODE':op.quality.trace_node,
                    'QUALITY_CHEMICAL_NAME':op.quality.chemical_name,'QUALITY_UNITS':op.quality.inpfile_units,
                    'VISCOSITY':op.hydraulic.viscosity,'DIFFUSIVITY':op.hydraulic.diffusivity,'SPECIFIC':op.hydraulic.specific_gravity,
                    'TRIALS':op.hydraulic.trials,'ACCURACY':op.hydraulic.accuracy,'HEADERROR':op.hydraulic.headerror,'FLOWCHANGE':op.hydraulic.flowchange,
                    'UNBALANCED':op.hydraulic.unbalanced,'UNBALANCED_VALUE':op.hydraulic.unbalanced_value,
                    'MINIMUM':op.hydraulic.minimum_pressure,'REQUIRED':op.hydraulic.required_pressure,'PRESSURE':op.hydraulic.pressure_exponent,
                    'PATTERN':op.hydraulic.pattern,'DEMAND_MULTIPLIER':op.hydraulic.demand_multiplier,'DEMAND_MODEL':op.hydraulic.demand_model,
                    'EMITTER':op.hydraulic.emitter_exponent,'TOLERANCE':op.quality.tolerance,'CHECKFREQ':op.hydraulic.checkfreq,
                    'MAXCHECK':op.hydraulic.maxcheck,'DAMPLIMIT':op.hydraulic.damplimit,'MAP':op.graphics.map_filename}
            return Response(status=status.HTTP_200_OK, data=data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def retrieve(self, request, pk=None):
        """Use this endpoint to read a specific option entry using its id"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            op = wn.options
            if pk == 'UNITS':
                data = {pk:op.hydraulic.inpfile_units}
            elif pk == 'HEADLOSS':
                data = {pk:op.hydraulic.headloss}
            elif pk == 'HYDRAULICS':
                data = {pk:op.hydraulic.hydraulics}
            elif pk == 'HYDRAULICS_FILENAME':
                data = {pk:op.hydraulic.hydraulics_filename}
            elif pk == 'QUALITY_PARAMETER':
                data = {pk:op.quality.parameter}
            elif pk == 'QUALITY_TRACE_NODE':
                data = {pk:op.quality.trace_node}
            elif pk == 'QUALITY_CHEMICAL_NAME':
                data = {pk:op.quality.chemical_name}
            elif pk == 'QUALITY_UNITS':
                data = {pk:op.quality.inpfile_units}
            elif pk == 'VISCOSITY':
                data = {pk:op.hydraulic.viscosity}
            elif pk == 'DIFFUSIVITY':
                data = {pk:op.hydraulic.diffusivity}
            elif pk == 'SPECIFIC':
                data = {pk: op.hydraulic.specific_gravity}
            elif pk == 'TRIALS':
                data = {pk: op.hydraulic.trials}
            elif pk == 'ACCURACY':
                data = {pk: op.hydraulic.accuracy}
            elif pk == 'HEADERROR':
                data = {pk: op.hydraulic.headerror}
            elif pk == 'FLOWCHANGE':
                data = {pk: op.hydraulic.flowchange}
            elif pk == 'UNBALANCED':
                data = {pk: op.hydraulic.unbalanced}
            elif pk == 'UNBALANCED_VALUE':
                data = {pk: op.hydraulic.unbalanced_value}
            elif pk == 'MINIMUM':
                data = {pk: op.hydraulic.minimum_pressure}
            elif pk == 'REQUIRED':
                data = {pk: op.hydraulic.required_pressure}
            elif pk == 'PRESSURE':
                data = {pk: op.hydraulic.pressure_exponent}
            elif pk == 'PATTERN':
                data = {pk: op.hydraulic.pattern}
            elif pk == 'DEMAND_MULTIPLIER':
                data = {pk: op.hydraulic.demand_multiplier}
            elif pk == 'DEMAND_MODEL':
                data = {pk: op.hydraulic.demand_model}
            elif pk == 'EMITTER':
                data = {pk: op.hydraulic.emitter_exponent}
            elif pk == 'TOLERANCE':
                data = {pk: op.quality.tolerance}
            elif pk == 'CHECKFREQ':
                data = {pk: op.hydraulic.checkfreq}
            elif pk == 'MAXCHECK':
                data = {pk: op.hydraulic.maxcheck}
            elif pk == 'DAMPLIMIT':
                data = {pk: op.hydraulic.damplimit}
            elif pk == 'MAP':
                data = {pk: op.graphics.map_filename}
            return Response(status=status.HTTP_200_OK, data=data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


#UPDATED, REMOVED create, update, destroy
class WaterPatternsViewSet(viewsets.ViewSet):
    """
        Information
        Use this API endpoint to read, create and update Patterns.
    """
    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def list(self, request):
        """Use this endpoint to read all the patterns data from the database"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            data = {'PATTERNS': wn.pattern_name_list}
            return Response(status=status.HTTP_200_OK, data=data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 404: openapi.Response('error, entry not found')})
    def retrieve(self, request, pk=None):
        """Use this endpoint to read a specific pattern entry using its id"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            data = {pk: wn.get_pattern(pk).multipliers}
            return Response(status=status.HTTP_200_OK, data=data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


#UPDATED, REMOVED update, create, destroy
class WaterPipesViewSet(viewsets.ViewSet):
    """
        Information
        Use this API endpoint to read, create and update Pipes.
    """
    serializer_class = serializers.WaterPipesSerializer
    queryset = models.WaterPipes.objects.all()
    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def list(self, request):
        """Use this endpoint to read all the pipes data from the database"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            return Response(status=status.HTTP_200_OK,data={'pipes': wn.pipe_name_list})
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: openapi.Response('ok, data returned'), 404: openapi.Response('error, entry not found')})
    def retrieve(self, request, pk=None):
        """Use this endpoint to read a specific pipe entry using its id"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            pipe = wn.get_link(pk)
            jresponse = {'name':pipe.name,'length':pipe.length,
                         'diameter': pipe.diameter, 'roughness':pipe.roughness, 'minor_loss':pipe.minor_loss,
                         'status':str(pipe.status),'start_node_name':pipe.start_node_name,'end_node_name':pipe.end_node_name,
                         'flow':pipe.flow,'initial_setting':pipe.initial_setting,
                         'initial_status':str(pipe.initial_status),'setting':pipe.setting,
                         'tag':pipe.tag,'vertices':pipe.vertices}
            return Response(status=status.HTTP_200_OK,data=jresponse)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


#UPDATED, REMOVED update, create, destroy
class WaterPumpsViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to read, create and update Pumps.
    """
    serializer_class = serializers.WaterPumpsSerializer
    queryset = models.WaterPumps.objects.all()

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def list(self, request):
        """Use this endpoint to read all the pumps data from the database"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            return Response(status=status.HTTP_200_OK, data={'pipes': wn.pump_name_list})
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 404: openapi.Response('error, entry not found')})
    def retrieve(self, request, pk=None):
        """Use this endpoint to read a specific pump entry using its id"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            pump = wn.get_link(pk)
            jresponse = {'name': pump.name,
                         'status': str(pump.status), 'start_node_name': pump.start_node_name,
                         'end_node_name': pump.end_node_name,
                         'flow': pump.flow, 'initial_setting': pump.initial_setting,
                         'initial_status': str(pump.initial_status),
                         'tag': pump.tag, 'vertices': pump.vertices}
            return Response(status=status.HTTP_200_OK, data=jresponse)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


#UPDATED, REMOVED create
class WaterReactionsViewSet(viewsets.ViewSet):
    """
        Information
        Use this API endpoint to read, create and update Reactions.
    """
    serializer_class = serializers.WaterReactionsSerializer

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def list(self, request):
        """Use this endpoint to read all the reactions data from the database"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            data = {'ORDER_BULK':wn.options.reaction.bulk_order,'ORDER_WALL':wn.options.reaction.wall_order,
                    'ORDER_TANK':wn.options.reaction.tank_order,'GLOBAL_BULK':wn.options.reaction.bulk_coeff,
                    'GLOBAL_WALL':wn.options.reaction.wall_coeff,'LIMITING':wn.options.reaction.limiting_potential,
                    'ROUGHNESS':wn.options.reaction.roughness_correl}
            return Response(status=status.HTTP_200_OK, data=data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def retrieve(self, request, pk=None):
        """Use this endpoint to read a specific reaction entry using its id"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            if pk == 'ORDER_BULK':
                return Response(status=status.HTTP_200_OK, data={'ORDER_BULK':wn.options.reaction.bulk_order})
            elif pk == 'ORDER_WALL':
                return Response(status=status.HTTP_200_OK, data={'ORDER_WALL':wn.options.reaction.wall_order})
            elif pk == 'ORDER_TANK':
                return Response(status=status.HTTP_200_OK, data={'ORDER_TANK': wn.options.reaction.tank_order})
            elif pk == 'GLOBAL_BULK':
                return Response(status=status.HTTP_200_OK, data={'GLOBAL_BULK': wn.options.reaction.bulk_coeff})
            elif pk == 'GLOBAL_WALL':
                return Response(status=status.HTTP_200_OK, data={'GLOBAL_WALL': wn.options.reaction.wall_coeff})
            elif pk == 'LIMITING':
                return Response(status=status.HTTP_200_OK, data={'LIMITING': wn.options.reaction.limiting_potential})
            elif pk == 'ROUGHNESS':
                return Response(status=status.HTTP_200_OK, data={'ROUGHNESS': wn.options.reaction.roughness_correl})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def update(self, request, pk=None):
        """Use this endpoint to update a reaction using its id"""
        serializer = serializers.WaterReactionsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                inp_file = 'basp/Water/Water.inp'
                wn = wntr.network.WaterNetworkModel(inp_file)
                if pk == 'ORDER_BULK':
                    wn.options.reaction.bulk_order = float(serializer.data.get('value'))
                    wn.write_inpfile(inp_file)
                    return Response(status=status.HTTP_200_OK)
                elif pk == 'ORDER_WALL':
                    wn.options.reaction.wall_order = float(serializer.data.get('value'))
                    wn.write_inpfile(inp_file)
                    return Response(status=status.HTTP_200_OK)
                elif pk == 'ORDER_TANK':
                    wn.options.reaction.tank_order = float(serializer.data.get('value'))
                    wn.write_inpfile(inp_file)
                    return Response(status=status.HTTP_200_OK)
                elif pk == 'GLOBAL_BULK':
                    wn.options.reaction.bulk_coeff = float(serializer.data.get('value'))
                    wn.write_inpfile(inp_file)
                    return Response(status=status.HTTP_200_OK)
                elif pk == 'GLOBAL_WALL':
                    wn.options.reaction.wall_coeff = float(serializer.data.get('value'))
                    wn.write_inpfile(inp_file)
                    return Response(status=status.HTTP_200_OK)
                elif pk == 'LIMITING':
                    wn.options.reaction.limiting_potential = float(serializer.data.get('value'))
                    wn.write_inpfile(inp_file)
                    return Response(status=status.HTTP_200_OK)
                elif pk == 'ROUGHNESS':
                    wn.options.reaction.roughness_correl = float(serializer.data.get('value'))
                    wn.write_inpfile(inp_file)
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def destroy(self, request, pk=None):
        """Use this endpoint to remove a reaction from the database using its id"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            if pk == 'ORDER_BULK':
                wn.options.reaction.bulk_order = float(0)
                wn.write_inpfile(inp_file)
                return Response(status=status.HTTP_200_OK)
            elif pk == 'ORDER_WALL':
                wn.options.reaction.wall_order = float(0)
                wn.write_inpfile(inp_file)
                return Response(status=status.HTTP_200_OK)
            elif pk == 'ORDER_TANK':
                wn.options.reaction.tank_order = float(0)
                wn.write_inpfile(inp_file)
                return Response(status=status.HTTP_200_OK)
            elif pk == 'GLOBAL_BULK':
                wn.options.reaction.bulk_coeff = float(0)
                wn.write_inpfile(inp_file)
                return Response(status=status.HTTP_200_OK)
            elif pk == 'GLOBAL_WALL':
                wn.options.reaction.wall_coeff = float(0)
                wn.write_inpfile(inp_file)
                return Response(status=status.HTTP_200_OK)
            elif pk == 'LIMITING':
                wn.options.reaction.limiting_potential = float(0)
                wn.write_inpfile(inp_file)
                return Response(status=status.HTTP_200_OK)
            elif pk == 'ROUGHNESS':
                wn.options.reaction.roughness_correl = float(0)
                wn.write_inpfile(inp_file)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


#UPDATED, REMOVED create, update, destroy
class WaterReportViewSet(viewsets.ViewSet):
    """
        Information
        Use this API endpoint to read, create and update Report.
    """
    serializer_class = serializers.WaterReportSerializer

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def list(self, request):
        """Use this endpoint to read all the reports data from the database"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            pagesize = wn.options.report.pagesize
            try:
                file = wn.options.report.file
            except:
                file = ''
            statusrep = wn.options.report.status
            summary = wn.options.report.summary
            energy = wn.options.report.energy
            nodes = wn.options.report.nodes
            links = wn.options.report.links
            report_params = wn.options.report.report_params
            data = {'pagesize':pagesize,'file':file,'status':statusrep,'summary':summary,'energy':energy,'nodes':nodes,
                    'links':links,'report_params':report_params}
            return Response(status=status.HTTP_200_OK, data=data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def retrieve(self, request, pk=None):
        """Use this endpoint to read a specific report entry using its id"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            if pk == 'pagesize':
                data = {'pagesize':wn.options.report.pagesize}
                return Response(status=status.HTTP_200_OK, data=data)
            elif pk == 'file':
                try:
                    data = {'file': wn.options.report.file}
                    return Response(status=status.HTTP_200_OK, data=data)
                except:
                    data = {'file': ''}
                    return Response(status=status.HTTP_200_OK, data=data)
            elif pk == 'status':
                data = {'status':wn.options.report.status}
                return Response(status=status.HTTP_200_OK, data=data)
            elif pk == 'summary':
                data = {'summary':wn.options.report.summary}
                return Response(status=status.HTTP_200_OK, data=data)
            elif pk == 'energy':
                data = {'energy':wn.options.report.energy}
                return Response(status=status.HTTP_200_OK, data=data)
            elif pk == 'nodes':
                data = {'nodes':wn.options.report.nodes}
                return Response(status=status.HTTP_200_OK, data=data)
            elif pk == 'links':
                data = {'links':wn.options.report.links}
                return Response(status=status.HTTP_200_OK, data=data)
            elif pk == 'report_params':
                data = {'report_params':wn.options.report.report_params}
                return Response(status=status.HTTP_200_OK, data=data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


#UPDATED, REMOVED update, create, destroy
class WaterReservoirsViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to read, create and update Reservoirs.
    """
    serializer_class = serializers.WaterReservoirsSerializer

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def list(self, request):
        """Use this endpoint to read all the reservoirs data from the database"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            return Response(status=status.HTTP_200_OK, data=wn.reservoir_name_list)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def retrieve(self, request, pk=None):
        """Use this endpoint to read a specific reservoir entry using its id"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            reservoir = wn.nodes[pk]
            data = {'reservoir':pk,'Head':reservoir.head_timeseries.base_value,'Pattern':reservoir.head_timeseries.pattern}
            return Response(status=status.HTTP_200_OK, data=data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


#UPDATED, REMOVED update, create, destroy
class WaterSourcesViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to read, create and update Sources.
    """
    serializer_class = serializers.WaterSourcesSerializer

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def list(self, request):
        """Use this endpoint to read all the sources data from the database"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            return Response(status=status.HTTP_200_OK, data=wn.source_name_list)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def retrieve(self, request, pk=None):
        """Use this endpoint to read a specific source entry using its id"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            source = wn.get_source(pk)
            data = {'name':source.name,'node_name':source.node_name,'source_type':source.source_type,
                    'base_value':source.strength_timeseries.base_value,
                    'pattern_name':source.strength_timeseries.pattern_name}
            return Response(status=status.HTTP_200_OK, data=data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


#UPDATED
class WaterClearDataView(viewsets.ViewSet):
    """
    Information

    Use this API endpoint to clear
    the database from EPANET inp file values
    """
    serializer_class = serializers.WaterClearDataSerializer
    test_param = openapi.Parameter('Clear', openapi.IN_QUERY, description="use true or false", type=openapi.TYPE_BOOLEAN)
    user_response = openapi.Response('Status OK')
    @swagger_auto_schema(manual_parameters=[test_param], responses={200: openapi.Response('ok, data cleared'), 400:openapi.Response('error, problem with POST request, data not cleared')})
    def create(self, request):
        """Use this API endpoint to clear the database from EPANET inp file values. Set Clear field to true for cleaning the database."""
        serializer = serializers.WaterClearDataSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.data.get('clear')
            if file.lower() == 'true':
                dbcommunication.mod_db_tables(databaseTables.waterDBtables('add'))
                dbcommunication.mod_db_tables(databaseTables.waterDBtables('delete'))
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#UPDATED
class WaterJSONFileView(viewsets.ViewSet):
    """
        Information
        Use this API endpoint to retrieve
        the EPANET JSON file generated from EPANET binary file
    """
    serializer_class = serializers.WaterOutputJSONSerializer
    def create(self, request):
        """"""
        serializer = serializers.WaterOutputJSONSerializer(data=request.data)
        if serializer.is_valid():
            experimentname = serializer.data.get('experimentname')
            existing_ex_names = list(models.ExperimentNames.objects.all())
            allthenames = []
            for value in existing_ex_names:
                allthenames.append(value.ex_name)
            if experimentname in allthenames:
                filename = "basp\\uploads\\"+str(experimentname)+"\\simulationdata.json"
                fin_filename = "simulationdata.json"
                response = FileResponse(open(filename, 'rb'))
                response['Content-Disposition'] = 'attachment; filename="%s"' % fin_filename
                return response
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#TODO
class WaterLoadView(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to load
        the EPANET inp file into the BaSP database
    """
    serializer_class = serializers.WaterLoadSerializer
    def list(self, request):
        """Returns a list of Water Start Features"""
        return Response({'Title': 'KIOS BaSP REST API for Water Simulations',
                         'information': 'Here you can load an EPANET inp file into the BaSP',
                         'details': 'File fields accepts the words ltown or new',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.WaterLoadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.data.get('file')
            if file == 'ltown':
                try:
                    # Create PostgreSQL database tables if they do not exist
                    dbcommunication.mod_db_tables(databaseTables.waterDBtables('add'))
                    # Delete any existing values from that tables
                    dbcommunication.mod_db_tables(databaseTables.waterDBtables('delete'))
                    # Read the EPANET Input (inp) file
                    #finalresult = watersim.readinputfile('basp/Water/Virtual_City_WaterNetwork.inp', databaseTables.epanetINPKeywords())
                    # Add EPANET Input (inp) file parameters into Python lists
                    #fullinputs = watersim.addinfotolists(finalresult, databaseTables.epanetINPFields())
                    # Add EPANET parameters into the PostgreSQL database
                    #watersim.addDataToDatabase(databaseTables.finalAllINPFields(), fullinputs)
                    shutil.copy2('basp/Water/Virtual_City_WaterNetwork.inp', 'basp/Water/Water.inp')
                    return Response({'status': 'ok', 'message': 'ltown inp file loaded'})
                except:
                    return Response({'status': 'error', 'message': 'ltown file cannot be loaded'})
            else:
                return Response({'status': 'error', 'message': 'Unknown file'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#UPDATED
class WaterStartView(viewsets.ViewSet):
    """
        Information
        Use this API endpoint to run an EPANET simulation.
        Values in the database will be used to create the EPANET inp file.
        You can provide details such as start/end date.
    """
    serializer_class = serializers.WaterStartSerializer
    def list(self, request):
        """Returns a list of Water Start Features"""
        existing_ex_names = list(models.ExperimentNames.objects.all())
        allthenames = []
        for value in existing_ex_names:
            allthenames.append(value.ex_name)
        return Response(status=status.HTTP_200_OK, data={'Title': 'KIOS BaSP REST API for Water Simulations',
                         'information': 'Here you can start an EPANET simulation',
                         'details': 'the values in the reserved list are not allowed as experiment names',
                         'reserved_list': allthenames})

    def post(self, request):
        """"""
        start_time = time.time()
        serializer = serializers.WaterStartSerializer(data=request.data)
        if serializer.is_valid():
            startdate = serializer.data.get('startdate')
            enddate = serializer.data.get('enddate')
            existing_ex_names = list(models.ExperimentNames.objects.all())
            allthenames = []
            for value in existing_ex_names:
                allthenames.append(value.ex_name)
            experimentname = serializer.data.get('experimentname')
            if experimentname not in allthenames:
                sensors = serializer.data.get('sensors')
                sensors = re.sub(r"[\n\t]*", "", sensors)
                final_sensors_json_file_contents = ""
                fs = FileSystemStorage()
                sensors = ContentFile(sensors)
                filename = fs.save(experimentname+'/test.json', sensors)
                f = default_storage.open(os.path.join(filename), 'r')
                with f as json_file:
                    final_sensors_json_file_contents = json.load(json_file)
                startdate_object = datetime.strptime(startdate, '%Y-%m-%d')
                enddate_object = datetime.strptime(enddate, '%Y-%m-%d')
                datediff = enddate_object - startdate_object
                days, seconds = datediff.days, datediff.total_seconds()
                hours = days * 24
                epoch1 = datetime.utcfromtimestamp(0)
                startdate_epoch = (startdate_object - epoch1).total_seconds() * 1000.0
                enddate_epoch = (enddate_object - epoch1).total_seconds() * 1000.0
                grafanaurl = "http://localhost:3001/d/GIfxrnEGz/water-sensors-basp?orgId=1&from="+str(int(startdate_epoch))+"&to="+str(int(enddate_epoch))
                if hours < 1:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={'startdate': startdate, 'enddate': enddate, 'message': 'startdate>enddate'})
                else:
                    try:
                        ex_name = serializer.data.get('experimentname')
                        #Get Report Timestep
                        inp_file = 'basp/Water/Water.inp'
                        wn = wntr.network.WaterNetworkModel(inp_file)
                        opts = wn.options
                        timestepinseconds = opts.time.report_timestep
                        #Put New Duration
                        wn.options.time.duration = int(seconds)
                        wn.write_inpfile('basp/Water/Water.inp')
                        # Run EPANET & Convert Bin to JSON wntr
                        watersim.epanetandbin2jsonwntr('basp/Water/Water.inp','basp/Water/jsonoutput.json')
                        time1 = time.time() - start_time
                        # Write EPANET JSON to PostgreSQL
                        watersim.readjsonwithfiles('basp/Water/jsonoutput.json', startdate_object, timestepinseconds, final_sensors_json_file_contents, ex_name)
                        # Save Experiment Name in the database
                        newname = models.ExperimentNames(ex_name=serializer.data.get('experimentname'), ex_sensor_filename=str(filename))
                        newname.save()
                        return Response(status=status.HTTP_200_OK, data={'startdate': startdate, 'enddate': enddate, 'message': 'simulation completed', 'interface': grafanaurl})#,'time1':time1,'timesecondsall':time.time() - start_time})
                    except:
                        return Response(status=status.HTTP_400_BAD_REQUEST, data={'startdate': startdate, 'enddate': enddate, 'message': 'simulation not completed'})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'experimentname is reserved'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#UPDATED
class WaterStartWntrView(viewsets.ViewSet):
    """
        Information
        Use this API endpoint to run an EPANET simulation.
        Values in the database will be used to create the EPANET inp file.
        You can provide details such as start/end date.
    """
    serializer_class = serializers.WaterStartSerializerWNTR
    def list(self, request):
        """Returns a list of Water Start Features"""
        existing_ex_names = list(models.ExperimentNames.objects.all())
        allthenames = []
        for value in existing_ex_names:
            allthenames.append(value.ex_name)
        return Response(status=status.HTTP_200_OK, data={'Title': 'KIOS BaSP REST API for Water Simulations',
                         'information': 'Here you can start a WNTR simulation',
                         'details': 'the values in the reserved list are not allowed as experiment names',
                         'reserved_list': allthenames})

    def post(self, request):
        """"""
        #start_time = time.time()
        serializer = serializers.WaterStartSerializerWNTR(data=request.data)
        if serializer.is_valid():
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            startdate = serializer.data.get('startdate')
            enddate = serializer.data.get('enddate')
            existing_ex_names = list(models.ExperimentNames.objects.all())
            allthenames = []
            for value in existing_ex_names:
                allthenames.append(value.ex_name)
            experimentname = serializer.data.get('experimentname')
            if experimentname not in allthenames:
                sensors = serializer.data.get('sensors')
                sensors = re.sub(r"[\n\t]*", "", sensors)
                fileleak = request.data.get('leakages')
                if fileleak is not None:
                    if len(fileleak) > 0:
                        try:
                            #inp_file = 'basp/Water/Water.inp'
                            #wn = wntr.network.WaterNetworkModel(inp_file)
                            wn = addleakages.addwaterleak(fileleak, wn)
                            #wn.write_inpfile('basp/Water/Water.inp')
                        except:
                            return Response(status=status.HTTP_400_BAD_REQUEST,data={'error': 'leakages file issue'})
                final_sensors_json_file_contents = ""
                fs = FileSystemStorage()
                sensors = ContentFile(sensors)
                filename = fs.save(experimentname+'/test.json', sensors)
                f = default_storage.open(os.path.join(filename), 'r')
                with f as json_file:
                    final_sensors_json_file_contents = json.load(json_file)
                startdate_object = datetime.strptime(startdate, '%Y-%m-%d')
                enddate_object = datetime.strptime(enddate, '%Y-%m-%d')
                datediff = enddate_object - startdate_object
                days, seconds = datediff.days, datediff.total_seconds()
                hours = days * 24
                epoch1 = datetime.utcfromtimestamp(0)
                startdate_epoch = (startdate_object - epoch1).total_seconds() * 1000.0
                enddate_epoch = (enddate_object - epoch1).total_seconds() * 1000.0
                grafanaurl = "http://localhost:3001/d/GIfxrnEGz/water-sensors-basp?orgId=1&from="+str(int(startdate_epoch))+"&to="+str(int(enddate_epoch))
                if hours < 1:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={'startdate': startdate, 'enddate': enddate, 'message': 'startdate>enddate'})
                else:
                    try:
                        ex_name = serializer.data.get('experimentname')
                        #Get Report Timestep

                        opts = wn.options
                        timestepinseconds = opts.time.report_timestep
                        #print(timestepinseconds)
                        #Put New Duration
                        wn.options.time.duration = int(seconds)
                        wn.write_inpfile('basp/Water/Water.inp')
                        # Run EPANET & Convert Bin to JSON wntr
                        watersim.wntr2jsonwntr(wn,'basp/Water/jsonoutput.json')
                        #time1 = time.time() - start_time
                        # Write EPANET JSON to PostgreSQL
                        watersim.readjsonwithfiles('basp/Water/jsonoutput.json', startdate_object, timestepinseconds, final_sensors_json_file_contents, ex_name)
                        # Save Experiment Name in the database
                        newname = models.ExperimentNames(ex_name=serializer.data.get('experimentname'), ex_sensor_filename=str(filename))
                        newname.save()
                        return Response(status=status.HTTP_200_OK, data={'startdate': startdate, 'enddate': enddate, 'message': 'simulation completed', 'water interface': grafanaurl})# 'transportation interface':'http://localhost:3001/d/4YdONpXGk/transportation?orgId=1&from=1617570000000&to=1617656399000'})
                    except:
                        return Response(status=status.HTTP_400_BAD_REQUEST, data={'startdate': startdate, 'enddate': enddate, 'message': 'simulation not completed'})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'experimentname is reserved'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#TODO
class WaterStepExecution(viewsets.ViewSet):
    """
            Information
            Use this API endpoint to run an EPANET simulation in Step Execution Mode.
            Values in the database will be used to create the EPANET inp file.
            You can provide details such as start/end date.
        """
    serializer_class = serializers.WaterStepExecutionSerializer
    def list(self, request):
        """Returns a list of Water Start Features"""
        return Response(status=status.HTTP_200_OK, data={'Title': 'KIOS BaSP REST API for Water Simulations',
                                                         'information': 'Here you can start an EPANET simulation. Please provide the following details',
                                                         'Startdate':'Initial date the simulation starts/started',
                                                         'Timestep':'(Integer) The timestep to be executed first',
                                                         'Iterations':'(Integer) The number of timesteps to be executed',
                                                         'Timestep size':'(Integer) The size of each timestep in seconds',
                                                         'Experiment name':'(String) The name of the experiment',
                                                         'Sensors':'The sensors json file'
                                                         })

    def post(self, request):
        """"""
        from datetime import timedelta
        start_time = time.time()
        serializer = serializers.WaterStepExecutionSerializer(data=request.data)
        if serializer.is_valid():
            startdate = serializer.data.get('startdate')
            timestep = int(serializer.data.get('timestep'))
            iterations = int(serializer.data.get('iterations'))
            timestep_size = int(serializer.data.get('timestep_size'))
            experiment_name = str(serializer.data.get('experiment_name'))
            sensors = serializer.data.get('sensors')
            sensors = re.sub(r"[\n\t]*", "", sensors)
            fs = FileSystemStorage()
            sensors = ContentFile(sensors)
            filename = fs.save(experiment_name + '/sensors.json', sensors)
            f = default_storage.open(os.path.join(filename), 'r')
            final_sensors_json_file_contents = ""
            with f as json_file:
                final_sensors_json_file_contents = json.load(json_file)
            startdate_object = datetime.strptime(startdate, '%Y-%m-%d')
            difffromthebeginning = timestep*timestep_size
            startdate_object = startdate_object + timedelta(seconds=difffromthebeginning)
            epoch1 = datetime.utcfromtimestamp(0)
            startdate_epoch = ((startdate_object - epoch1).total_seconds() * 1000.0)
            enddate_epoch = (startdate_epoch + (timestep_size*iterations*1000))
            grafanaurl = "http://localhost:3001/d/GIfxrnEGz/water-sensors-basp?orgId=1&from=" + str(int(startdate_epoch)) + "&to=" + str(int(enddate_epoch))+str("&refresh=5s")
            start_clocktime = int(timestep*timestep_size)%86400
            if iterations < 1:
                return Response(status=status.HTTP_400_BAD_REQUEST,data={'message': 'iterations must be greater than 0'})
            else:
                try:
                    ex_name = serializer.data.get('experiment_name')
                    # Get Report Timestep
                    inp_file = 'basp/Water/Water.inp'
                    wn = wntr.network.WaterNetworkModel(inp_file)
                    opts = wn.options
                    timestepinseconds = timestep_size
                    # Put New Duration
                    wn.options.time.duration = int(iterations*timestep_size)
                    wn.options.time.start_clocktime = start_clocktime
                    wn.options.time.report_timestep = timestep_size
                    wn.write_inpfile('basp/Water/Water.inp')
                    # Run EPANET & Convert Bin to JSON wntr
                    watersim.epanetandbin2jsonwntr('basp/Water/Water.inp', 'basp/Water/jsonoutput.json')
                    time1 = time.time() - start_time
                    # Write EPANET JSON to PostgreSQL
                    #TODO Modify for step execution
                    #print('basp/Water/jsonoutput.json', startdate_object, timestepinseconds,final_sensors_json_file_contents, ex_name)
                    watersim.readjsonwithfilesstep('basp/Water/jsonoutput.json', startdate_object, timestepinseconds,final_sensors_json_file_contents, ex_name)
                    # Save Experiment Name in the database
                    if not models.ExperimentNames.objects.filter(ex_name=ex_name).exists():
                        newname = models.ExperimentNames(ex_name=ex_name,ex_sensor_filename=str(filename))
                        newname.save()
                    return Response(status=status.HTTP_200_OK, data={'startdate': startdate, 'timestep': timestep,'iterations':iterations,
                                                                     'message': 'simulation completed',
                                                                     'interface': grafanaurl, 'time1': time1,
                                                                     'timesecondsall': time.time() - start_time})
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST,data={'message': 'simulation not completed'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#UPDATED, REMOVED update, create, destroy
class WaterTanksViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to read, create and update Tanks.
    """
    serializer_class = serializers.WaterTanksSerializer

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def list(self, request):
        """Use this endpoint to read all the tanks data from the database"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            return Response(status=status.HTTP_200_OK, data=wn.tank_name_list)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def retrieve(self, request, pk=None):
        """Use this endpoint to read a specific tank entry using its id"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            tank = wn.get_node(pk)
            data = {'ID':tank.name,'Elev':tank.elevation,'InitLvl':tank.init_level,'MinLvl':tank.min_level,
                    'MaxLvl':tank.max_level,'Diam':tank.diameter,'MinVol':tank.min_vol,'VolCurve':tank.vol_curve}
            return Response(status=status.HTTP_200_OK, data=data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


#UPDATED, REMOVED update, create, destroy
class WaterValvesViewSet(viewsets.ViewSet):
    """
        Information
        Use this API endpoint to read, create and update Valves.
    """
    serializer_class = serializers.WaterValvesSerializer

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def list(self, request):
        """Use this endpoint to read all the valve data from the database"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            return Response(status=status.HTTP_200_OK, data=wn.valve_name_list)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def retrieve(self, request, pk=None):
        """Use this endpoint to read a specific valve entry using its id"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            valve = wn.get_link(pk)
            data = {'name': pk,'node1': valve.start_node_name,'node2': valve.end_node_name,
                    'diam': valve.diameter,'vtype': valve.valve_type,'set': valve._setting,'mloss': valve.minor_loss}
            return Response(status=status.HTTP_200_OK, data=data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


#UPDATED, REMOVED create, update, destroy
class WaterTimesViewSet(viewsets.ViewSet):
    """
        Information
        Use this API endpoint to read, create and update Times.
    """
    serializer_class = serializers.WaterTimesSerializer

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def list(self, request):
        """Use this endpoint to read all the times data from the database"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            opts = wn.options
            data={'duration':opts.time.duration,'hydraulic_timestep':opts.time.hydraulic_timestep,
                  'quality_timestep':opts.time.quality_timestep,'rule_timestep':opts.time.rule_timestep,
                  'pattern_timestep':opts.time.pattern_timestep,'pattern_start':opts.time.pattern_start,
                  'report_timestep':opts.time.report_timestep,'report_start':opts.time.report_start,
                  'start_clocktime':opts.time.start_clocktime,'statistic':opts.time.statistic}
            return Response(status=status.HTTP_200_OK, data=data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def retrieve(self, request, pk=None):
        """Use this endpoint to read a specific time entry using its id"""
        try:
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            opts = wn.options
            if pk == 'duration':
                data = {'duration': opts.time.duration}
                return Response(status=status.HTTP_200_OK, data=data)
            elif pk == 'hydraulic_timestep':
                data = {'hydraulic_timestep': opts.time.hydraulic_timestep}
                return Response(status=status.HTTP_200_OK, data=data)
            elif pk == 'quality_timestep':
                data = {'quality_timestep': opts.time.quality_timestep}
                return Response(status=status.HTTP_200_OK, data=data)
            elif pk == 'rule_timestep':
                data = {'rule_timestep': opts.time.rule_timestep}
                return Response(status=status.HTTP_200_OK, data=data)
            elif pk == 'pattern_timestep':
                data = {'pattern_timestep': opts.time.pattern_timestep}
                return Response(status=status.HTTP_200_OK, data=data)
            elif pk == 'pattern_start':
                data = {'pattern_start': opts.time.pattern_start}
                return Response(status=status.HTTP_200_OK, data=data)
            elif pk == 'report_timestep':
                data = {'report_timestep': opts.time.report_timestep}
                return Response(status=status.HTTP_200_OK, data=data)
            elif pk == 'report_start':
                data = {'report_start': opts.time.report_start}
                return Response(status=status.HTTP_200_OK, data=data)
            elif pk == 'start_clocktime':
                data = {'start_clocktime': opts.time.start_clocktime}
                return Response(status=status.HTTP_200_OK, data=data)
            elif pk == 'statistic':
                data = {'statistic': opts.time.statistic}
                return Response(status=status.HTTP_200_OK, data=data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class WaterOutputLinksViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to read EPANET simulation output for links.
        Using the 'links' field, a list of links can be specified for relevant results. If 'links' field is left empty then results for all the links will be returned.
        Using the 'fields' field, a list of fields can be specified for relevant results. If 'fields' field is left empty then all the fields will be returned.
        Using the 'resolution' field, the instrument (sensor) resolution can be specified. If 'resolution' field is left empty then simulation results will be returned.
        Using the 'drop' field, the drop rate in percentage can be specified. If 'drop' field is left empty then all the results will be returned.
    """
    serializer_class = serializers.WaterOutputLinksSerializer

    def list(self, request):
        """Returns a list of the details of output links"""
        return Response({'Title': 'KIOS BaSP REST API for Water Simulations',
                         'information': 'Here you can retrieve EPANET simulation Links Output',
                         'links': 'provide a list of links, or leave empty to receive all of them',
                         'links example': ['p1', 'p2', 'p3'],
                         'fields': 'provide a list of fields, or leave empty to receive all of them',
                         'fields allowed': ['linkfriction', 'linkheadloss', 'linkquality', 'linkreactiontime', 'linksetting', 'linkstatus', 'linkvelocity'],
                         'resolution': 'provide a float between 0.0 and 1.0 to specify sensor resolution or leave empty to get original value',
                         'drop': 'provide a value between 0 and 100 to specify the random drop rate'})

    def post(self, request):
        serializer = serializers.WaterOutputLinksSerializer(data=request.data)
        if serializer.is_valid():
            links = serializer.data.get('links')
            if links is not None:
                final_query = "SELECT DISTINCT linkid FROM water_output_links_values"
                alllinkidsdup = dbcommunication.read_db_values(final_query)
                alllinkidslist = []
                for val4 in alllinkidsdup:
                    alllinkidslist.append(val4[0])
                if "[" not in links or "]" not in links:
                    return Response({'status': 'error', 'message': 'links must be a list'})
                else:
                    newlinks = ast.literal_eval(links)
                    newlinks = [str(n).strip() for n in newlinks]
                    result = all(elem in alllinkidslist for elem in newlinks)
                    if not result:
                        return Response({'status': 'error', 'message': 'invalid links', 'allowed_links': alllinkidslist})
            fields = serializer.data.get('fields')
            if fields is not None:
                if "[" not in fields or "]" not in fields:
                    return Response({'status': 'error', 'message': 'fields must be a list'})
                else:
                    newfields = ast.literal_eval(fields)
                    newfields = [str(n).strip() for n in newfields]
                    allowedfields = ['linkfriction', 'linkheadloss', 'linkquality', 'linkreactiontime', 'linksetting', 'linkstatus', 'linkvelocity']
                    result = all(elem in allowedfields for elem in newfields)
                    if not result:
                        return Response({'status': 'error', 'message': 'invalid fields', 'allowed_fields': allowedfields})
            resolution = serializer.data.get('resolution')
            drop = serializer.data.get('drop')
            final_values = []
            if links is None:
                if fields is None:
                    final_query = "SELECT * FROM water_output_links_values"
                    final_values = dbcommunication.read_db_values(final_query)
                else:
                    specificfields = ', '.join(newfields)
                    final_query = "SELECT linkid, readingtime, "+specificfields+" FROM water_output_links_values"
                    final_values = dbcommunication.read_db_values(final_query)
            elif links is not None:
                if fields is None:
                    for value in newlinks:
                        final_query = "SELECT * FROM water_output_links_values WHERE linkid='" + value + "'"
                        linksinner = dbcommunication.read_db_values(final_query)
                        for val in linksinner:
                            final_values.append(val)
                else:
                    for value in newlinks:
                        specificfields = ', '.join(newfields)
                        final_query = "SELECT id, linkid, readingtime, " + specificfields + " FROM water_output_links_values WHERE linkid='" + value + "'"
                        linksinner = dbcommunication.read_db_values(final_query)
                        for val in linksinner:
                            final_values.append(val)
            nodesinresults = []
            for value in final_values:
                if value[1] not in nodesinresults:
                    nodesinresults.append(value[1])
            resultstoreturn = {}
            if drop is not None:
                population = [0, 1]
                probabilityof1 = float(1) - (float(drop)/100)
                weights = [float(drop)/100, probabilityof1]
            for node in nodesinresults:
                nodevalues = {}
                for value in final_values:
                    if node == value[1]:
                        v = value[2].strftime("%Y-%m-%dT%H:%M:%S")
                        restvalstub = value[3:]
                        restvallist = []
                        for v1 in restvalstub:
                            if resolution is not None:
                                try:
                                    if (float(v1) / float(resolution)).is_integer():
                                        resultwithrest = v1
                                    else:
                                        resultwithrest = float(v1) - math.fmod(float(v1), float(resolution))
                                        t001 = str(resolution).split('.')
                                        flformat = "{:."+str(len(t001[1]))+"f}"
                                        resultwithrest = flformat.format(resultwithrest)
                                    if drop is not None:
                                        resultwithrest = float(choices(population, weights)[0]) * float(resultwithrest)
                                        restvallist.append(float(resultwithrest))
                                    else:
                                        restvallist.append(float(resultwithrest))
                                except:
                                    if drop is not None:
                                        if choices(population, weights)[0] == 0:
                                            restvallist.append('')
                                        else:
                                            restvallist.append(v1)
                                    else:
                                        restvallist.append(v1)
                            else:
                                if drop is not None:
                                    try:
                                        resultwithrest = float(choices(population, weights)[0]) * float(v1)
                                        restvallist.append(resultwithrest)
                                    except:
                                        if choices(population, weights)[0] == 0:
                                            restvallist.append('')
                                        else:
                                            restvallist.append(v1)
                                else:
                                    restvallist.append(v1)
                        nodevalues[v] = restvallist
                resultstoreturn[node] = nodevalues
            allowedfields = ['linkfriction', 'linkheadloss', 'linkquality', 'linkreactiontime', 'linksetting','linkstatus', 'linkvelocity']
            if fields is None:
                outputformat = "{'link': {'measure_time': ["+', '.join(allowedfields)+"],...},...}"
            else:
                outputformat = "{'link': {'measure_time': ["+', '.join(newfields)+"],...},...}"
            return Response(
                {'status': 'ok', 'outputformat': outputformat, 'values': resultstoreturn})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WaterOutputSensorsValuesViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to read EPANET simulation output for sensors.
        Use the 'experimentname' field, to provide the name of the experiment in order to get the correct experiment readings.
        Use the 'sensorid' field, to provide a list of sensor ids in order to get the relevant sensors values.
    """
    serializer_class = serializers.WaterOutputSensorsValuesSerializer

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned')})
    def list(self, request):
        """Returns a list of Water Start Features"""
        return Response(status=status.HTTP_200_OK,data={'Title': 'KIOS BaSP REST API for Water Simulations',
                         'information': 'Here you can retrieve EPANET simulation sensor readings',
                         'experimentname': 'provide the experiment name',
                         'sensorid': 'provide a list of sensor ids, or leave empty to receive all of them',
                         'sensorid_example': ['sensor_1', 'sensor_2']})

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def post(self, request):
        serializer = serializers.WaterOutputSensorsValuesSerializer(data=request.data)
        if serializer.is_valid():
            experimentname = serializer.data.get('experimentname')
            sensorid = serializer.data.get('sensorid')
            existing_ex_names = list(models.ExperimentNames.objects.all())
            allthenames = []
            for value in existing_ex_names:
                allthenames.append(value.ex_name)
            if experimentname in allthenames:
                if sensorid is not None:
                    final_query = "SHOW TAG VALUES ON virtual_city FROM water_output_"+str(experimentname)+"_scada_sensors WITH KEY=sensorid"
                    allsensorsids = dbcommunication.read_influxdb_values(final_query)
                    allsensoridslist = []
                    for val4 in allsensorsids:
                        allsensoridslist.append(val4[1])
                    if "[" not in sensorid or "]" not in sensorid:
                        return Response(status=status.HTTP_400_BAD_REQUEST,data={'message': 'sensorid must be a list'})
                    else:
                        try:
                            newlinks = ast.literal_eval(sensorid)
                            newlinks = [str(n).strip() for n in newlinks]
                            result = all(elem in allsensoridslist for elem in newlinks)
                            if not result:
                                return Response(status=status.HTTP_400_BAD_REQUEST,data={'message': 'invalid sensor ids', 'allowed_sensors': allsensoridslist})
                            else:
                                finalresult = []
                                for value in newlinks:
                                    final_query = "SELECT time, sensor_value FROM water_output_"+str(experimentname)+"_scada_sensors WHERE sensorid='"+value+"'"
                                    allsensorsids = dbcommunication.read_influxdb_values(final_query)
                                    entry = {}
                                    entry['sensorid'] = value
                                    finalvalues = []
                                    for reading in allsensorsids:
                                        indivalue = {}
                                        indivalue['timestamp'] = reading[0]
                                        indivalue['value'] = reading[1]
                                        finalvalues.append(indivalue)
                                    entry['values'] = finalvalues
                                    finalresult.append(entry)
                                return Response(status=status.HTTP_200_OK,data=finalresult)
                        except:
                            return Response(status=status.HTTP_400_BAD_REQUEST,data = {'message': 'invalid sensor ids','allowed_sensors': allsensoridslist})
                else:
                    final_query = "SHOW TAG VALUES ON virtual_city FROM water_output_"+str(experimentname)+"_scada_sensors WITH KEY=sensorid"
                    allsensorsids = dbcommunication.read_influxdb_values(final_query)
                    allsensoridslist = []
                    for val4 in allsensorsids:
                        allsensoridslist.append(val4[1])
                    finalresult = []
                    for value in allsensoridslist:
                        final_query = "SELECT time, sensor_value FROM water_output_" + str(experimentname) + "_scada_sensors WHERE sensorid='" + value + "'"
                        allsensorsids = dbcommunication.read_influxdb_values(final_query)
                        entry = {}
                        entry['sensorid'] = value
                        finalvalues = []
                        for reading in allsensorsids:
                            indivalue = {}
                            indivalue['timestamp'] = reading[0]
                            indivalue['value'] = reading[1]
                            finalvalues.append(indivalue)
                        entry['values'] = finalvalues
                        finalresult.append(entry)
                    return Response(status=status.HTTP_200_OK,data = finalresult)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST,data = {'message': 'experimentname does not exist'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WaterOutputNodesViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to read EPANET simulation output for nodes.
        Using the 'nodes' field, a list of nodes can be specified for relevant results. If 'nodes' field is left empty then results for all the nodes will be returned.
        Using the 'fields' field, a list of fields can be specified for relevant results. If 'fields' field is left empty then all the fields will be returned.
        Using the 'resolution' field, the instrument (sensor) resolution can be specified. If 'resolution' field is left empty then simulation results will be returned.
        Using the 'drop' field, the drop rate in percentage can be specified. If 'drop' field is left empty then all the results will be returned.
    """
    serializer_class = serializers.WaterOutputNodesSerializer

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned')})
    def list(self, request):
        """Returns a list of Water Start Features"""
        return Response(status=status.HTTP_200_OK,data={'Title': 'KIOS BaSP REST API for Water Simulations',
                         'information': 'Here you can retrieve EPANET simulation nodes Output',
                         'nodes': 'provide a list of nodes, or leave empty to receive all of them',
                         'nodes example': ['n1', 'n2', 'n3'],
                         'fields': 'provide a list of fields, or leave empty to receive all of them',
                         'fields allowed': ['nodedemand', 'nodehead', 'nodepressure', 'nodequality'],
                         'resolution': 'provide a float between 0.0 and 1.0 to specify sensor resolution or leave empty to get original value',
                         'drop': 'provide a value between 0 and 100 to specify the random drop rate'})

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def post(self, request):
        serializer = serializers.WaterOutputNodesSerializer(data=request.data)
        if serializer.is_valid():
            nodes = serializer.data.get('nodes')
            if nodes is not None:
                final_query = "SELECT DISTINCT nodeid FROM water_output_nodes_values"
                alllinkidsdup = dbcommunication.read_db_values(final_query)
                alllinkidslist = []
                for val4 in alllinkidsdup:
                    alllinkidslist.append(val4[0])
                if "[" not in nodes or "]" not in nodes:
                    return Response(status=status.HTTP_400_BAD_REQUEST,data={'message': 'nodes must be a list'})
                else:
                    newlinks = ast.literal_eval(nodes)
                    newlinks = [str(n).strip() for n in newlinks]
                    result = all(elem in alllinkidslist for elem in newlinks)
                    if not result:
                        return Response(status=status.HTTP_400_BAD_REQUEST,data={'message': 'invalid nodes', 'allowed_nodes': alllinkidslist})
            fields = serializer.data.get('fields')
            if fields is not None:
                if "[" not in fields or "]" not in fields:
                    return Response(status=status.HTTP_400_BAD_REQUEST,data={'message': 'fields must be a list'})
                else:
                    newfields = ast.literal_eval(fields)
                    newfields = [str(n).strip() for n in newfields]
                    allowedfields = ['nodedemand', 'nodehead', 'nodepressure', 'nodequality']
                    result = all(elem in allowedfields for elem in newfields)
                    if not result:
                        return Response(status=status.HTTP_400_BAD_REQUEST,data={'message': 'invalid fields', 'allowed_fields': allowedfields})
            resolution = serializer.data.get('resolution')
            drop = serializer.data.get('drop')
            final_values = []
            if nodes is None:
                if fields is None:
                    final_query = "SELECT * FROM water_output_nodes_values"
                    final_values = dbcommunication.read_db_values(final_query)
                else:
                    specificfields = ', '.join(newfields)
                    final_query = "SELECT nodeid, readingtime, " + specificfields + " FROM water_output_nodes_values"
                    final_values = dbcommunication.read_db_values(final_query)
            elif nodes is not None:
                if fields is None:
                    for value in newlinks:
                        final_query = "SELECT * FROM water_output_nodes_values WHERE nodeid='" + value + "'"
                        linksinner = dbcommunication.read_db_values(final_query)
                        for val in linksinner:
                            final_values.append(val)
                else:
                    for value in newlinks:
                        specificfields = ', '.join(newfields)
                        final_query = "SELECT id, nodeid, readingtime, " + specificfields + " FROM water_output_nodes_values WHERE nodeid='" + value + "'"
                        linksinner = dbcommunication.read_db_values(final_query)
                        for val in linksinner:
                            final_values.append(val)
            nodesinresults = []
            for value in final_values:
                if value[1] not in nodesinresults:
                    nodesinresults.append(value[1])
            resultstoreturn = {}
            if drop is not None:
                population = [0, 1]
                probabilityof1 = float(1) - (float(drop) / 100)
                weights = [float(drop) / 100, probabilityof1]
            for node in nodesinresults:
                nodevalues = {}
                for value in final_values:
                    if node == value[1]:
                        v = value[2].strftime("%Y-%m-%dT%H:%M:%S")
                        restvalstub = value[3:]
                        restvallist = []
                        for v1 in restvalstub:
                            if resolution is not None:
                                try:
                                    if (float(v1) / float(resolution)).is_integer():
                                        resultwithrest = v1
                                    else:
                                        resultwithrest = float(v1) - math.fmod(float(v1), float(resolution))
                                        t001 = str(resolution).split('.')
                                        flformat = "{:." + str(len(t001[1])) + "f}"
                                        resultwithrest = flformat.format(resultwithrest)
                                    if drop is not None:
                                        resultwithrest = float(choices(population, weights)[0]) * float(resultwithrest)
                                        restvallist.append(float(resultwithrest))
                                    else:
                                        restvallist.append(float(resultwithrest))
                                except:
                                    if drop is not None:
                                        if choices(population, weights)[0] == 0:
                                            restvallist.append('')
                                        else:
                                            restvallist.append(v1)
                                    else:
                                        restvallist.append(v1)
                            else:
                                if drop is not None:
                                    try:
                                        resultwithrest = float(choices(population, weights)[0]) * float(v1)
                                        restvallist.append(resultwithrest)
                                    except:
                                        if choices(population, weights)[0] == 0:
                                            restvallist.append('')
                                        else:
                                            restvallist.append(v1)
                                else:
                                    restvallist.append(v1)
                        nodevalues[v] = restvallist
                resultstoreturn[node] = nodevalues
            allowedfields = ['nodedemand', 'nodehead', 'nodepressure', 'nodequality']
            if fields is None:
                outputformat = "{'node': {'measure_time': [" + ', '.join(allowedfields) + "],...},...}"
            else:
                outputformat = "{'node': {'measure_time': [" + ', '.join(newfields) + "],...},...}"
            return Response(status=status.HTTP_200_OK,data={'outputformat': outputformat, 'values': resultstoreturn})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#UPDATED
class WaterAddLeakViewSet(viewsets.ViewSet):
    """
        Information
        Use this API endpoint to add leak
    """
    serializer_class = serializers.WaterLeakSerializer

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned')})
    def list(self, request):
        """Returns a list of Water Start Features"""
        return Response(status=status.HTTP_200_OK,data={'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Returns the lane's length in m.",
                          'area': 'Area of the leak in m^2',
                          'start_time':'Start time of the leak in seconds.',
                          'end_time':'Time at which the leak is fixed in seconds',
                          })

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned'), 400: openapi.Response('error, bad request')})
    def post(self, request):
        """"""
        serializer = serializers.WaterLeakSerializer(data=request.data)
        if serializer.is_valid():
            file = request.data.get('file')
            try:
                inp_file = 'basp/Water/Water.inp'
                wn = wntr.network.WaterNetworkModel(inp_file)
                data = yaml.load (file, Loader = yaml.FullLoader)
                Start_Time = datetime.strptime (data['times']['StartTime'], '%Y-%m-%d %H:%M')
                leakages = data['leakages']
                for i in leakages:
                    items = i.split (', ')
                    pipe = items[0]
                    area = 3.14159 * (float (items[3]) / 2) ** 2
                    start = datetime.strptime (str (items[1]), '%Y-%m-%d %H:%M')
                    end = datetime.strptime (str (items[2]), '%Y-%m-%d %H:%M')
                    start_sec = (start - Start_Time).total_seconds ()
                    end_sec = (end - Start_Time).total_seconds ()
                    wn = wntr.morph.split_pipe (wn, pipe, pipe + '_B', pipe + '_leak_node')
                    leak_node = wn.get_node (pipe + '_leak_node')
                    #emitter coefficient
                    leak_node.add_leak (wn, area = area, start_time = start_sec, end_time = end_sec)
                wn.write_inpfile('basp/Water/Water.inp')
                return Response(status=status.HTTP_200_OK,data='Done')
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WaterEarthquakeViewSet(viewsets.ViewSet):
    """
        Information
        Use this API endpoint to add earthquake
    """
    serializer_class = serializers.WaterEarthquakeSerializer

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned')})
    def list(self, request):
        """"""
        return Response(status=status.HTTP_200_OK,data={'Title': 'KIOS BaSP REST API for Water Simulations',
                          'epicenterx': "x location",
                          'epicentery': 'y location',
                          'magnitude':'Richter scale',
                          ' depth ':'m, shallow depth',
                          })

    @swagger_auto_schema (
        responses = {200: openapi.Response ('ok, data returned'), 400: openapi.Response ('error, bad request')})
    def post (self, request):
        """"""
        serializer = serializers.WaterEarthquakeSerializer (data = request.data)
        if serializer.is_valid ():
            try:
                inp_file = 'basp/Water/Water.inp'
                print('in1')
                wn = wntr.network.WaterNetworkModel(inp_file)
                print('wn')

                epicenterx = serializer.data.get('epicenterx')
                epicentery = serializer.data.get('epicentery')
                magnitude = serializer.data.get('magnitude')
                depth = serializer.data.get('depth')
                epicenter = (epicenterx,epicentery)
                print( epicenter )
                earthquake = wntr.scenario.Earthquake (epicenter, magnitude, depth)
                return Response (status = status.HTTP_200_OK, data = earthquake)
            except Exception as e:
                print('exception e ')
                print(e)
                return Response (status = status.HTTP_400_BAD_REQUEST)
        else:
            print('else error')
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class WaterPowerOutageViewSet(viewsets.ViewSet):
    """
        Information
        Use this API endpoint to add power outage
    """
    serializer_class = serializers.WaterEarthquakeSerializer

    @swagger_auto_schema(
        responses={200: openapi.Response('ok, data returned')})
    def list(self, request):
        """"""
        return Response(status=status.HTTP_200_OK,data={'Title': 'KIOS BaSP REST API for Water Simulations',
                          'link': "pump name",
                          'start_time': 'start time in seconds',
                          'end_time':'end time in seconds',
                          })

    @swagger_auto_schema (
        responses = {200: openapi.Response ('ok, data returned'), 400: openapi.Response ('error, bad request')})
    def post (self, request):
        """"""
        serializer = serializers.WaterPowerOutageSerializer (data = request.data)
        if serializer.is_valid ():
            try:
                inp_file = 'basp/Water/Water.inp'
                print('in1')
                wn = wntr.network.WaterNetworkModel(inp_file)
                print('wn')

                link = serializer.data.get('link')
                start_time = serializer.data.get('start_time')
                end_time = serializer.data.get('end_time')

                pump = wn.get_link(link)
                pump.add_outage (wn, start_time, end_time)
                return Response (status = status.HTTP_200_OK, data = 'Done')
            except Exception as e:
                print('exception e ')
                print(e)
                return Response (status = status.HTTP_400_BAD_REQUEST)
        else:
            print('else error')
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)


#TODO
class TransportationLaneGetLengthViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get the lane's length in m
    """
    serializer_class = serializers.TransportationLaneGetSerializer
    def list(self, request):
        """Returns a list of Water Start Features"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns the lane's length in m.",
                         'laneID': 'Provide a lane id',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationLaneGetSerializer(data=request.data)
        if serializer.is_valid():
            laneID = serializer.data.get('laneID')
            
            try:
                tracioutput = traci.lane.getLength(laneID)
            except Exception as e:
                return Response ({'status': 'Error','message': str (e)})
            else:
                return Response ({'status': 'ok', 'data': tracioutput})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationLaneGetMaxSpeedViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get the lane's maximum allowed speed
    """
    serializer_class = serializers.TransportationLaneGetSerializer
    def list(self, request):
        """Returns a list of Water Start Features"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns the maximum allowed speed on the lane in m/s.",
                         'laneID': 'Provide a lane id',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationLaneGetSerializer(data=request.data)
        if serializer.is_valid():
            laneID = serializer.data.get('laneID')
            
            try:
                tracioutput = traci.lane.getMaxSpeed(laneID)
            except Exception as e:
                return Response ({'status': 'Error','message': str (e)})
            else:
                return Response ({'status': 'ok', 'data': tracioutput})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationLaneGetCO2EmissionViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get the CO2 emission in mg for the last time step on the given lane.
    """
    serializer_class = serializers.TransportationLaneGetSerializer
    def list(self, request):
        """Returns a list of Water Start Features"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns the CO2 emission in mg for the last time step on the given lane.",
                         'laneID': 'Provide a lane id',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationLaneGetSerializer(data=request.data)
        if serializer.is_valid():
            laneID = serializer.data.get('laneID')
            
            try:
                tracioutput = traci.lane.getCO2Emission(laneID)
            except Exception as e:
                return Response ({'status': 'Error','message': str (e)})
            else:
                return Response ({'status': 'ok', 'data': tracioutput})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationLaneGetCOEmissionViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get the CO emission in mg for the last time step on the given lane.
    """
    serializer_class = serializers.TransportationLaneGetSerializer
    def list(self, request):
        """Returns a list of Water Start Features"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns the CO emission in mg for the last time step on the given lane.",
                         'laneID': 'Provide a lane id',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationLaneGetSerializer(data=request.data)
        if serializer.is_valid():
            laneID = serializer.data.get ('laneID')
            
            try:
                tracioutput = traci.lane.getCOEmission (laneID)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'data': tracioutput})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationLaneGetHCEmissionViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get the HC emission in mg for the last time step on the given lane.
    """
    serializer_class = serializers.TransportationLaneGetSerializer
    def list(self, request):
        """Returns a list of Water Start Features"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns the HC emission in mg for the last time step on the given lane.",
                         'laneID': 'Provide a lane id',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationLaneGetSerializer(data=request.data)
        if serializer.is_valid():
            laneID = serializer.data.get('laneID')
            
            try:
                tracioutput = traci.lane.getHCEmission (laneID)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'data': tracioutput})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationLaneGetPMxEmissionViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get the particular matter emission in mg for the last time step on the given lane.
    """
    serializer_class = serializers.TransportationLaneGetSerializer
    def list(self, request):
        """Returns a list of Water Start Features"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns the particular matter emission in mg for the last time step on the given lane.",
                         'laneID': 'Provide a lane id',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationLaneGetSerializer(data=request.data)
        if serializer.is_valid():
            laneID = serializer.data.get('laneID')
            
            try:
                tracioutput = traci.lane.getPMxEmission (laneID)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'data': tracioutput})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationLaneGetNOxEmissionViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get the NOx emission in mg for the last time step on the given lane.
    """
    serializer_class = serializers.TransportationLaneGetSerializer
    def list(self, request):
        """Returns a list of Water Start Features"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns the NOx emission in mg for the last time step on the given lane.",
                         'laneID': 'Provide a lane id',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationLaneGetSerializer(data=request.data)
        if serializer.is_valid():
            laneID = serializer.data.get('laneID')
            
            try:
                tracioutput = traci.lane.getNOxEmission (laneID)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'data': tracioutput})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationLaneGetFuelConsumptionViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get the fuel consumption in ml for the last time step on the given lane.
    """
    serializer_class = serializers.TransportationLaneGetSerializer
    def list(self, request):
        """Returns a list of Water Start Features"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns the fuel consumption in ml for the last time step on the given lane.",
                         'laneID': 'Provide a lane id',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationLaneGetSerializer(data=request.data)
        if serializer.is_valid():
            laneID = serializer.data.get('laneID')
            
            try:
                tracioutput = traci.lane.getFuelConsumption (laneID)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'data': tracioutput})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationLaneGetNoiseEmissionViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get the noise emission in db for the last time step on the given lane.
    """
    serializer_class = serializers.TransportationLaneGetSerializer
    def list(self, request):
        """Returns a list of Water Start Features"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns the noise emission in db for the last time step on the given lane.",
                         'laneID': 'Provide a lane id',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationLaneGetSerializer(data=request.data)
        if serializer.is_valid():
            laneID = serializer.data.get('laneID')
            
            try:
                tracioutput = traci.lane.getNoiseEmission(laneID)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'data': tracioutput})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationLaneGetElectricityConsumptionViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get the electricity consumption in ml for the last time step.
    """
    serializer_class = serializers.TransportationLaneGetSerializer
    def list(self, request):
        """Returns a list of Water Start Features"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns the electricity consumption in ml for the last time step.",
                         'laneID': 'Provide a lane id',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationLaneGetSerializer(data=request.data)
        if serializer.is_valid():
            laneID = serializer.data.get('laneID')
            
            try:
                tracioutput = traci.lane.getElectricityConsumption(laneID)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'data': tracioutput})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationLaneGetIDListViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get a list of all lanes in the network
    """
    def list(self, request):
        """Returns a list of all objects in the network"""
        try:
            tracioutput = traci.lane.getIDList()
        except Exception as e:
            return Response ({'status': 'Error', 'message': str (e)})
        else:
            return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns a list of all lanes in the network.",
                         'data':tracioutput,
                         }
                        )


class TransportationLaneGetIDCountViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get the number of all lanes in the network
    """

    def list(self, request):
        """Returns a list of all objects in the network"""
        try:
            tracioutput = traci.lane.getIDCount()
        except Exception as e:
            return Response ({'status': 'Error', 'message': str (e)})
        else:
            return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns the number of all lanes in the network.",
                         'data' : tracioutput,
                         }
                        )

class TransportationTrafficlightGetIDListViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get a list of all traffic lights in the network
    """
    def list(self, request):
        """Returns a list of all objects in the network"""
        try:
            traciout = traci.trafficlight.getIDList()
        except Exception as e:
            return Response ({'status': 'Error', 'message': str (e)})
        else:
            return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns a list of all traffic lights in the network.",
                         'data':traciout
                         }
                        )



class TransportationTrafficlightGetIDCountViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get the count of all traffic lights in the network
    """
    def list(self, request):
        """Returns a list of all objects in the network"""
        try:
            traciout = traci.trafficlight.getIDCount()
        except Exception as e:
            return Response ({'status': 'Error', 'message': str (e)})
        else:
            return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns the count of all traffic lights in the network.",
                         'data':traciout
                         }
                        )


class TransportationTrafficlightGetRedYellowGreenStateViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get the traffic light state
    """
    serializer_class = serializers.TransportationTrafficlightGetSerializer
    def list(self, request):
        """Returns a list of Water Start Features"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns the named tl's state as a tuple of light definitions from rugGyYoO, "
                                        "for red, yed-yellow, green, yellow, off, where lower case letters mean that "
                                        "the stream has to decelerate.",
                         'tlsID': 'Provide a traffic light id',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationTrafficlightGetSerializer(data=request.data)
        if serializer.is_valid():
            tlsID = serializer.data.get('tlsID')
            
            try:
                tracioutput = traci.trafficlight.getRedYellowGreenState(tlsID)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'data': tracioutput})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleGetIDCountViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get the number of vehicles currently running within the scenario
    """
    def list(self,request):
        """Returns the number of currently loaded objects"""
        try:
            tracioutput = traci.vehicle.getIDCount()
            # 
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)})
        else:
            return Response({'Title':'KIOS BaSP REST API for Transportation Simulations',
                             'information': 'Returns the number of vehicles currently running within the scenario',
                             'data': tracioutput}
                            )


class TransportationTrafficlightGetPhaseDurationViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get the total duration of the current phase (in seconds). This value
        is not affected by the elapsed or remaining duration of the current phase.
    """
    serializer_class = serializers.TransportationTrafficlightGetSerializer
    def list(self, request):
        """Returns a list of Water Start Features"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns the total duration of the current phase (in seconds). This value "
                                        "is not affected by the elapsed or remaining duration of the current phase.",
                         'tlsID': 'Provide a traffic light id',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationTrafficlightGetSerializer(data=request.data)
        if serializer.is_valid():
            tlsID = serializer.data.get('tlsID')
            
            try:
                tracioutput = traci.trafficlight.getPhaseDuration(tlsID)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'data': tracioutput})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationTrafficlightGetPhaseViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get the index of the current phase within the list of all phases of
        the current program.
    """
    serializer_class = serializers.TransportationTrafficlightGetSerializer
    def list(self, request):
        """Returns a list of Water Start Features"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns the index of the current phase within the list of all phases of the current program.",
                         'tlsID': 'Provide a traffic light id',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationTrafficlightGetSerializer(data=request.data)
        if serializer.is_valid():
            tlsID = serializer.data.get('tlsID')
            
            try:
                tracioutput = traci.trafficlight.getPhase(tlsID)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'data': tracioutput})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationVehicleGetIDListViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get a list of ids of all vehicles currently running within the scenario
    """
    serializer_class = serializers.TransportationVehicleGetIDListSerializer
    def list(self, request):
        ###
        try:
            tracioutput = traci.vehicle.getIDList()
        except Exception as e:
            return Response({'status': 'Error', 'message': str(e)})

        ###
        """Returns a list of ids of all vehicles currently running within the scenario"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns a list of ids of all vehicles currently running within the scenario",
                         'data':tracioutput
                         }
                        )


class TransportationTrafficlightSetRedYellowGreenStateViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to set the named tl's state as a tuple of light definitions.
    """
    serializer_class = serializers.TransportationTrafficlightSetRedYellowGreenStateSerializer
    def list(self, request):
        """Returns a list of Water Start Features"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the named tl's state as a tuple of light definitions from "
                                        "rugGyYuoO, for red, red-yellow, green, yellow, off, where lower "
                                        "case letters mean that the stream has to decelerate.",
                         'tlsID': 'Provide a traffic light id',
                         'state': "A tuple of light definitions from "
                                  "rugGyYuoO, for red, red-yellow, green, yellow, off, where lower "
                                  "case letters mean that the stream has to decelerate."
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationTrafficlightSetRedYellowGreenStateSerializer(data=request.data)
        if serializer.is_valid():
            tlsID = serializer.data.get('tlsID')
            state = serializer.data.get('state')
            try:
                traciout = traci.trafficlight.setRedYellowGreenState(tlsID,state)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': tlsID + " " + state})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationTrafficlightSetLinkStateViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to set the state for the given tls and link index.
    """
    serializer_class = serializers.TransportationTrafficlightSetLinkStateSerializer
    def list(self, request):
        """Returns a list of Water Start Features"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the state for the given tls and link index.",
                         'tlsID': 'Provide a traffic light id',
                         'state': 'The state must be one of rRgGyYoOu for red, red-yellow, green, yellow, '
                                  'off, where lower case letters mean that the stream has to decelerate.',
                         'tlsLinkIndex': 'The link index is shown in the GUI when setting the appropriate junction visualization option.'
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationTrafficlightSetLinkStateSerializer(data=request.data)
        if serializer.is_valid():
            tlsID = serializer.data.get('tlsID')
            tlsLinkIndex = serializer.data.get('tlsLinkIndex')
            state = serializer.data.get('state')
            try:
                traciout = traci.trafficlight.setLinkState (tlsID,tlsLinkIndex,state)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': tlsID + " " + str(tlsLinkIndex) + " " + state})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationTrafficlightSetPhaseViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to switch to the phase with the given index in the list of all phases for
        the current program.
    """
    serializer_class = serializers.TransportationTrafficlightSetPhaseSerializer
    def list(self, request):
        """Returns a list of Water Start Features"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Switches to the phase with the given index in the list of all phases for the current program.",
                         'tlsID': 'Provide a traffic light id',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationTrafficlightSetPhaseSerializer(data=request.data)
        if serializer.is_valid():
            tlsID = serializer.data.get('tlsID')
            index = serializer.data.get('index')

            try:
                traciout = traci.trafficlight.setPhase(tlsID,index)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': tlsID + " " + str(index)})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationTrafficlightSetPhaseDurationViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to set the remaining phase duration of the current phase in seconds.
    """
    serializer_class = serializers.TransportationTrafficlightSetPhaseDurationSerializer

    def list(self, request):
        """Returns a list of Water Start Features"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Set the remaining phase duration of the current phase in seconds."
                                        "This value has no effect on subsquent repetitions of this phase.",
                         'vehID': 'Provide a vehicle id',
                         }
                        )

    def post(self, request):
        """"""
        serializer = serializers.TransportationTrafficlightSetPhaseDurationSerializer(data=request.data)
        if serializer.is_valid():
            tlsID = serializer.data.get('tlsID')
            phaseDuration = serializer.data.get('phaseDuration')

            try:
                traciout = traci.trafficlight.setPhaseDuration (tlsID, phaseDuration)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': tlsID + " " + str(phaseDuration)})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationVehicleGetSpeedViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get the speed of the named vehicle within the last step [m/s]
    """
    serializer_class = serializers.TransportationVehicleGetSerializer
    def list(self, request):
        """Returns the speed of the named vehicle within the last step [m/s]"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns the (longitudinal) speed in m/s of the named vehicle within the last step.",
                         'vehID': 'Provide a vehicle id',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleGetSerializer(data=request.data)
        if serializer.is_valid():
            vehID = serializer.data.get('vehID')
            
            try:
                tracioutput = traci.vehicle.getSpeed(vehID)
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)})
            else:
                if (tracioutput==-1073741824.0):
                    return Response({'status': 'error'})
                else:
                    return Response({'status': 'ok', 'message': tracioutput })

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleGetAccelerationViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get the acceleration in the previous time step
    """
    serializer_class = serializers.TransportationVehicleGetSerializer
    def list(self, request):
        """Returns the acceleration in m/s^2 of the named vehicle within the last step."""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns the acceleration in m/s^2 of the named vehicle within the last step",
                         'vehID': 'Provide a vehicle id',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleGetSerializer(data=request.data)
        if serializer.is_valid():
            vehID = serializer.data.get('vehID')
            
            try:
                tracioutput = traci.vehicle.getAcceleration(vehID)
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)})
            else:
                if (tracioutput == -1073741824.0):
                    return Response({'status': 'error'})
                else:
                    return Response({'status': 'ok', 'message': tracioutput})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleGetPositionViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get the position(two doubles) of the named vehicle (center of the front bumper) within the last step [m,m]
    """
    serializer_class = serializers.TransportationVehicleGetSerializer
    def list(self, request):
        """Returns the position of the named vehicle within the last step [m,m]"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns the position of the named vehicle within the last step [m,m].",
                         'vehID': 'Provide a vehicle id',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleGetSerializer(data=request.data)
        if serializer.is_valid():
            vehID = serializer.data.get('vehID')
            
            try:
                tracioutput = traci.vehicle.getPosition(vehID)
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)})
            else:
                if (-1073741824.0 in tracioutput):
                    return Response({'status': 'error'})
                else:
                    return Response({'status': 'ok', 'message': tracioutput})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleGetCO2EmissionViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get Vehicle's CO2 emissions in mg/s during this time step, to get the value for one step multiply with the step length
    """
    serializer_class = serializers.TransportationVehicleGetSerializer
    def list(self, request):
        """Returns the CO2 emission in mg/s for the last time step.
            Multiply by the step length to get the value for one step."""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns the CO2 emission in mg/s for the last time step. Multiply by the step length to get the value for one step.",
                         'vehID': 'Provide a vehicle id',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleGetSerializer(data=request.data)
        if serializer.is_valid():
            vehID = serializer.data.get('vehID')
            
            try:
                tracioutput = traci.vehicle.getCO2Emission(vehID)
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)})
            else:
                if (tracioutput==-1073741824.0):
                    return Response({'status': 'error'})
                else:
                    return Response({'status': 'ok', 'message': tracioutput})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleGetCOEmissionViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get Vehicle's CO emissions in mg/s during this time step, to get the value for one step multiply with the step length
    """
    serializer_class = serializers.TransportationVehicleGetSerializer
    def list(self, request):
        """Returns the CO emission in mg/s for the last time step.
            Multiply by the step length to get the value for one step."""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns the CO emission in mg/s for the last time step. Multiply by the step length to get the value for one step.",
                         'vehID': 'Provide a vehicle id',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleGetSerializer(data=request.data)
        if serializer.is_valid():
            vehID = serializer.data.get('vehID')
            
            try:
                tracioutput = traci.vehicle.getCOEmission(vehID)
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)})
            else:
                if (tracioutput == -1073741824.0):
                    return Response({'status': 'error'})
                else:
                    return Response({'status': 'ok', 'message': tracioutput})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleGetHCEmissionViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get Vehicle's HC emissions in mg/s during this time step, to get the value for one step multiply with the step length
    """
    serializer_class = serializers.TransportationVehicleGetSerializer
    def list(self, request):
        """Returns the HC emission in mg/s for the last time step.
            Multiply by the step length to get the value for one step."""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns the HC emission in mg/s for the last time step. Multiply by the step length to get the value for one step.",
                         'vehID': 'Provide a vehicle id',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleGetSerializer(data=request.data)
        if serializer.is_valid():
            vehID = serializer.data.get('vehID')
            
            try:
                tracioutput = traci.vehicle.getHCEmission(vehID)
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)})
            else:
                if (tracioutput == -1073741824.0):
                    return Response({'status': 'error'})
                else:
                    return Response({'status': 'ok', 'message': tracioutput})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleGetPMxEmissionViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get Vehicle's PMx emissions in mg/s during this time step, to get the value for one step multiply with the step length
    """
    serializer_class = serializers.TransportationVehicleGetSerializer
    def list(self, request):
        """Returns the particular matter emission in mg/s for the last time step.
            Multiply by the step length to get the value for one step."""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns the particular matter emission emission in mg/s for the last time step. Multiply by the step length to get the value for one step.",
                         'vehID': 'Provide a vehicle id',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleGetSerializer(data=request.data)
        if serializer.is_valid():
            vehID = serializer.data.get('vehID')
            
            try:
                tracioutput = traci.vehicle.getPMxEmission(vehID)
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)})
            else:
                if (tracioutput == -1073741824.0):
                    return Response({'status': 'error'})
                else:
                    return Response({'status': 'ok', 'message': tracioutput})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleGetNOxEmissionViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get Vehicle's NOx emissions in mg/s during this time step, to get the value for one step multiply with the step length
    """
    serializer_class = serializers.TransportationVehicleGetSerializer
    def list(self, request):
        """Returns the NOx emission in mg/s for the last time step.
            Multiply by the step length to get the value for one step."""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns the NOx emission in mg/s for the last time step. Multiply by the step length to get the value for one step.",
                         'vehID': 'Provide a vehicle id',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleGetSerializer(data=request.data)
        if serializer.is_valid():
            vehID = serializer.data.get('vehID')
            
            try:
                tracioutput = traci.vehicle.getNOxEmission(vehID)
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)})
            else:
                if (tracioutput == -1073741824.0):
                    return Response({'status': 'error'})
                else:
                    return Response({'status': 'ok', 'message': tracioutput})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleGetFuelConsumptionViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get Vehicle's fuel consumption in ml/s during this time step, to get the value for one step multiply with the step length
    """
    serializer_class = serializers.TransportationVehicleGetSerializer
    def list(self, request):
        """Returns the NOx emission in mg/s for the last time step.
            Multiply by the step length to get the value for one step."""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns the fuel consumption in ml/s for the last time step. Multiply by the step length to get the value for one step.",
                         'vehID': 'Provide a vehicle id',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleGetSerializer(data=request.data)
        if serializer.is_valid():
            vehID = serializer.data.get('vehID')
            
            try:
                tracioutput = traci.vehicle.getFuelConsumption(vehID)
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)})
            else:
                if (tracioutput == -1073741824.0):
                    return Response({'status': 'error'})
                else:
                    return Response({'status': 'ok', 'message': tracioutput})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleGetNoiseEmissionViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get Noise generated by the vehicle in dBA
    """
    serializer_class = serializers.TransportationVehicleGetSerializer
    def list(self, request):
        """Returns the noise emission in db for the last time step."""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns the noise emission in db for the last time step.",
                         'vehID': 'Provide a vehicle id',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleGetSerializer(data=request.data)
        if serializer.is_valid():
            vehID = serializer.data.get('vehID')
            
            try:
                tracioutput = traci.vehicle.getNoiseEmission(vehID)
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)})
            else:
                if (tracioutput == -1073741824.0):
                    return Response({'status': 'error'})
                else:
                    return Response({'status': 'ok', 'message': tracioutput})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleGetElectricityConsumptionViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get Vehicle's electricity consumption in Wh/s during this time step, to get the value for one step multiply with the step length
    """
    serializer_class = serializers.TransportationVehicleGetSerializer
    def list(self, request):
        """Returns the electricity consumption in Wh/s for the last time step.
            Multiply by the step length to get the value for one step."""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns the electricity consumption in Wh/s for the last time step. Multiply by the step length to get the value for one step.",
                         'vehID': 'Provide a vehicle id',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleGetSerializer(data=request.data)
        if serializer.is_valid():
            vehID = serializer.data.get('vehID')
            
            try:
                tracioutput = traci.vehicle.getElectricityConsumption(vehID)
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)})
            else:
                if (tracioutput == -1073741824.0):
                    return Response({'status': 'error'})
                else:
                    return Response({'status': 'ok', 'message': tracioutput})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleStateSetStopViewSet(viewsets.ViewSet):
    """
            Information

           Lets the vehicle stop at the given edge, at the given position and lane.
           The vehicle will stop for the given duration. Re-issuing a stop command with the same lane and position allows changing the duration.
           Setting the duration to 0 cancels an existing stop.
        """
    serializer_class= serializers.TransportationVehicleStateSetStopSerializer
    def list(self, request):
        """Adds or modifies a stop with the given parameters."""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Adds or modifies a stop with the given parameters.",
                         'vehID': 'Provide a vehicle id',
                         'edgeID': 'Provide an edge id',
                         'pos': 'Provide a position',
                         'laneIndex':'Provide the lane Index',
                         'duration':'How long the vehicle will stop',
                         'flags':'',
                         'startPos':'Provide the start position in seconds',
                         'until':' in seconds',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleStateSetStopSerializer(data=request.data)
        if serializer.is_valid():
            vehID = serializer.data.get('vehID')
            edgeID = serializer.data.get('edgeID')
            pos = serializer.data.get('pos')
            laneIndex = serializer.data.get('laneIndex')
            duration = serializer.data.get('duration')
            flags = serializer.data.get('flags')
            startPos = serializer.data.get('startPos')
            until = serializer.data.get('until')
            
            try:
                tracioutput = traci.vehicle.setStop(vehID,edgeID,pos,laneIndex,duration,flags,startPos,until)
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)})
            else:
                return Response({'status': 'ok', 'message': "Successful"})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationVehicleStateSetBusStopViewSet (viewsets.ViewSet):
    """
            Information

           Lets the vehicle stop at the given edge, at the given position and lane.
           The vehicle will stop for the given duration. Re-issuing a stop command with the same lane and position allows changing the duration.
           Setting the duration to 0 cancels an existing stop.
        """
    serializer_class = serializers.TransportationVehicleStateSetBusStopSerializer

    def list (self, request):
        """Adds or modifies a bus stop with the given parameters. The duration and the until attribute are in seconds."""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Adds or modifies a bus stop with the given parameters. The duration and the until attribute are in seconds.",
                          'vehID': 'Provide a vehicle id',
                          'stopID': 'Provide a stop id',
                          'duration': 'How long the vehicle will stop',
                          'flags': '',
                          'until': ' in seconds',
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleStateSetBusStopSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            stopID = serializer.data.get ('stopID')
            duration = serializer.data.get ('duration')
            flags = serializer.data.get ('flags')
            until = serializer.data.get ('until')

            try:
                tracioutput = traci.vehicle.setBusStop (vehID, stopID, duration, until, flags)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})


        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleStateSetContainerStopViewSet (viewsets.ViewSet):
    """
            Information

           Lets the vehicle stop at the given edge, at the given position and lane.
           The vehicle will stop for the given duration. Re-issuing a stop command with the same lane and position allows changing the duration.
           Setting the duration to 0 cancels an existing stop.
        """
    serializer_class = serializers.TransportationVehicleStateSetContainerStopSerializer

    def list (self, request):
        """Adds or modifies a container stop with the given parameters. The duration and the until attribute are in seconds."""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Adds or modifies a container stop with the given parameters. The duration and the until attribute are in seconds.",
                          'vehID': 'Provide a vehicle id',
                          'stopID': 'Provide a stop id',
                          'duration': 'How long the vehicle will stop',
                          'flags': '',
                          'until': ' in seconds',
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleStateSetContainerStopSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            stopID = serializer.data.get ('stopID')
            duration = serializer.data.get ('duration')
            flags = serializer.data.get ('flags')
            until = serializer.data.get ('until')

            try:
                tracioutput = traci.vehicle.setContainerStop (vehID, stopID, duration, until, flags)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})


        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleStateSetChargingStopViewSet (viewsets.ViewSet):
    """
            Information

           Lets the vehicle stop at the given edge, at the given position and lane.
           The vehicle will stop for the given duration. Re-issuing a stop command with the same lane and position allows changing the duration.
           Setting the duration to 0 cancels an existing stop.
        """
    serializer_class = serializers.TransportationVehicleStateSetChargingStopSerializer

    def list (self, request):
        """Adds or modifies a bus stop with the given parameters. The duration and the until attribute are in seconds."""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Adds or modifies a stop at a chargingStation with the given parameters. The duration and the until attribute are in seconds.",
                          'vehID': 'Provide a vehicle id',
                          'stopID': 'Provide a stop id',
                          'duration': 'How long the vehicle will stop',
                          'flags': '',
                          'until': ' in seconds',
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleStateSetChargingStopSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            stopID = serializer.data.get ('stopID')
            duration = serializer.data.get ('duration')
            flags = serializer.data.get ('flags')
            until = serializer.data.get ('until')

            try:
                tracioutput = traci.vehicle.setChargingStationStop (vehID, stopID, duration, until, flags)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})


        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleStateSetParkingAreaStopViewSet (viewsets.ViewSet):
    """
            Information

           Lets the vehicle stop at the given edge, at the given position and lane.
           The vehicle will stop for the given duration. Re-issuing a stop command with the same lane and position allows changing the duration.
           Setting the duration to 0 cancels an existing stop.
        """
    serializer_class = serializers.TransportationVehicleStateSetParkingAreaStopSerializer

    def list (self, request):
        """Adds or modifies a stop at a parkingArea with the given parameters. The duration and the until attribute are in seconds"""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Adds or modifies a stop at a parkingArea with the given parameters. The duration and the until attribute are in seconds",
                          'vehID': 'Provide a vehicle id',
                          'stopID': 'Provide a stop id',
                          'duration': 'How long the vehicle will stop',
                          'flags': '',
                          'until': ' in seconds',
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleStateSetParkingAreaStopSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            stopID = serializer.data.get ('stopID')
            duration = serializer.data.get ('duration')
            flags = serializer.data.get ('flags')
            until = serializer.data.get ('until')

            try:
                tracioutput = traci.vehicle.setParkingAreaStop (vehID, stopID, duration, until, flags)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})


        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleStateChangeTargetViewSet (viewsets.ViewSet):
    """
            Information
           The vehicle's destination edge is set to the given. The route is rebuilt.
        """
    serializer_class = serializers.TransportationVehicleStateChangeTargetSerializer

    def list (self, request):
        """Adds or modifies a bus stop with the given parameters. The duration and the until attribute are in seconds."""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "The vehicle's destination edge is set to the given edge id. The route is rebuilt.",
                          'vehID': 'Provide a vehicle id',
                          'edgeID': 'Provide an edge id'
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleStateChangeTargetSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            edgeID = serializer.data.get('edgeID')

            try:
                tracioutput = traci.vehicle.changeTarget (vehID, edgeID)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})


        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleStateSetRouteIDViewSet (viewsets.ViewSet):
    """
            Information
           Assigns the named route to the vehicle, assuming a) the named route exists, and b) it starts on the edge the vehicle is currently at(1)(2).
        """
    serializer_class = serializers.TransportationVehicleStateSetRouteIdSerializer

    def list (self, request):
        """Adds or modifies a bus stop with the given parameters. The duration and the until attribute are in seconds."""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Changes the vehicles route to the route with the given id.",
                          'vehID': 'Provide a vehicle id',
                          'RouteID': 'Provide a route id'
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleStateSetRouteIdSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            routeID = serializer.data.get('routeID')

            try:
                tracioutput = traci.vehicle.changeTarget (vehID, routeID)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})


        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class TransportationVehicleStateSetRouteViewSet (viewsets.ViewSet):
    """
        Information
        Assigns the list of edges as the vehicle's new route assuming the first edge given is the one the vehicle is curently at(1)(2)
    """
    serializer_class = serializers.TransportationVehicleStateSetRouteSerializer

    def list (self, request):
        """"""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "changes the vehicle route to given edges list. The first edge in the list has to be the one that the vehicle is at at the moment.",
                          'vehID': 'Provide a vehicle id',
                          'edgeList': 'provide a list of edges',
                          'edgeList_example': ['1', '2', '4', '6', '7']
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleStateSetRouteSerializer (data = request.data)
        print('post')
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            print(vehID)
            edgeList = serializer.data.get ('route')
            print(edgeList)
            # dclasses = disallowedClasses.strip ('][').split (', ')
            if "[" not in edgeList or "]" not in edgeList:
                return Response ({'status': 'error', 'message': 'edgeList must be a list'})
            else:
                try:
                    dclasses = ast.literal_eval (edgeList)
                except:
                    return Response ({'status': 'Error', 'message': 'Give a list as in the example format',
                                      'edgeList_example': ['1', '2', '4', '6', '7']})
                try:
                    traci.vehicle.setRoute (vehID, dclasses)
                except Exception as e:
                    return Response ({'status': 'Error', 'message': str (e)})
                else:
                    return Response ({'status': 'ok', 'vehID': vehID, 'edgeList': dclasses})


        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleRerouteParkingAreaViewSet (viewsets.ViewSet):
    """
            Information
           Changes the next parking area in parkingAreaID, updates the vehicle route, and preserve consistency in case of passengers/containers on board
        """
    serializer_class = serializers.TransportationVehicleRerouteParkingAreaSerializer

    def list (self, request):
        """Adds or modifies a bus stop with the given parameters. The duration and the until attribute are in seconds."""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Changes the next parking area in parkingAreaID, updates the vehicle route,and preserve consistency in case of passengers/containers on board.",
                          'vehID': 'Provide a vehicle id',
                          'parkingAreaID': 'Provide a parkingArea ID'
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleRerouteParkingAreaSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            parkingAreaID = serializer.data.get('parkingAreaID')

            try:
                tracioutput = traci.vehicle.rerouteParkingArea (vehID, parkingAreaID)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})


        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleStateSetAdaptedTraveltimeViewSet (viewsets.ViewSet):
    """
            Information

           Inserts the information about the travel time (in seconds) of edge "edgeID" valid from begin time to end time (in seconds) into the vehicle's internal edge weights container.
        """
    serializer_class = serializers.TransportationVehicleStatesetAdaptedTraveltimeSerializer

    def list (self, request):
        """Adds or modifies a bus stop with the given parameters. The duration and the until attribute are in seconds."""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Inserts the information about the travel time of edge 'edgeID' valid from begin time to end time into the vehicle's internal edge weights container.If the time is not specified, any previously set values for that edge are removed."
                            " If begTime or endTime are not specified the value is set for the whole simulation duration.",
                          'vehID': 'Provide a vehicle id',
                          'edgeID': 'Provide an edge id',
                          'time': 'travel time in seconds',
                          'begTime': 'Begin time in seconds',
                          'endTime': 'End time in seconds',
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleStatesetAdaptedTraveltimeSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            edgeID = serializer.data.get ('edgeID')
            time = serializer.data.get ('time')
            begTime = serializer.data.get ('begTime')
            endTime = serializer.data.get ('endTime')

            try:
                tracioutput = traci.vehicle.setAdaptedTraveltime (vehID, edgeID, time, begTime, endTime)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})


        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleStatesetEffortViewSet (viewsets.ViewSet):
    """
            Information
        Inserts the information about the effort of edge "edgeID" valid from begin time to end time (in seconds) into the vehicle's internal edge weights container.        """

    serializer_class = serializers.TransportationVehicleStateSetEffortSerializer

    def list (self, request):
        """Adds or modifies a bus stop with the given parameters. The duration and the until attribute are in seconds."""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Inserts the information about the effort of edge'edgeID' valid from"
                            "begin time to end time into the vehicle's internal edge weights"
                            "container.If the time is not specified, any previously set values for that edge"
                            "are removed."
                            "If begTime or endTime are not specified the value is set for the whole simulation duration.",
                          'vehID': 'Provide a vehicle id',
                          'edgeID': 'Provide an edge id',
                          'effort': 'effort',
                          'begTime': 'Begin time in seconds',
                          'endTime': 'End time in seconds',
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleStateSetEffortSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            edgeID = serializer.data.get ('edgeID')
            effort = serializer.data.get ('effort')
            begTime = serializer.data.get ('begTime')
            endTime = serializer.data.get ('endTime')

            try:
                tracioutput = traci.vehicle.setEffort(vehID, edgeID, effort, begTime, endTime)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})


        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleStateSetSignalsViewSet (viewsets.ViewSet):
    """
            Information
            Sets a new state of signal."""
    serializer_class = serializers.TransportationVehicleStatesetSignalsSerializer

    def list (self, request):
        """Adds or modifies a bus stop with the given parameters. The duration and the until attribute are in seconds."""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Sets an integer encoding the state of the vehicle's signals.",
                          'vehID': 'Provide a vehicle id',
                          'signals': 'integer encoding the state of the vehicles signals',
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleStatesetSignalsSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            signals = serializer.data.get('signals')

            try:
                tracioutput = traci.vehicle.setSignals(vehID, signals)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})


        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleStatesetRoutingModeViewSet (viewsets.ViewSet):
    """
            Information
            Sets the routing mode (0: default, 1: aggregated)"""
    serializer_class = serializers.TransportationVehicleStatesetRoutingModeSerializer

    def list (self, request):
        """Adds or modifies a bus stop with the given parameters. The duration and the until attribute are in seconds."""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Sets the current routing mode:"
                            "tc.ROUTING_MODE_DEFAULT    : use weight storages and fall-back to edge speeds (default)"
                            "tc.ROUTING_MODE_AGGREGATED : use global smoothed travel times from device.rerouting",
                          'vehID': 'Provide a vehicle id',
                          'routingMode': 'Provide the current routing mode',
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleStatesetRoutingModeSerializer(data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            routingMode = serializer.data.get('routingMode')

            try:
                tracioutput = traci.vehicle.setRoutingMode(vehID, routingMode)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})


        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleStatesetMoveToViewSet (viewsets.ViewSet):
    """
            Information
            Moves the vehicle to a new position along the current route"""
    serializer_class = serializers.TransportationVehicleStateMoveToSerializer

    def list (self, request):
        """Moves the vehicle to a new position along the current route"""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Move a vehicle to a new position along it's current route.",
                          'vehID': 'Provide a vehicle id',
                          'laneID': 'Provide the lane id',
                          'pos':'Provide the new position',
                          'reason':'',
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleStateMoveToSerializer(data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            laneID = serializer.data.get('laneID')
            pos = serializer.data.get ('pos')
            reason = serializer.data.get ('reason')

            try:
                tracioutput = traci.vehicle.moveTo(vehID, laneID, pos, reason)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})


        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class TransportationVehicleStateResumeViewSet (viewsets.ViewSet):
    """
            Information
           Resumes the vehicle from the current stop (throws an error if the vehicle is not stopped).
        """
    serializer_class = serializers.TransportationVehicleStateResumeSerializer

    def list (self, request):
        """Adds or modifies a bus stop with the given parameters. The duration and the until attribute are in seconds."""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Resumes the vehicle from the current stop (throws an error if the vehicle is not stopped).",
                          'vehID': 'Provide a vehicle id',
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleStateResumeSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')

            try:
                tracioutput = traci.vehicle.resume (vehID)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})


        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleStateChangeLaneViewSet(viewsets.ViewSet):
    """
            Information

           Forces a lane change to the lane with the given index;
           if successful, the lane will be chosen for the given amount of time (in seconds).
        """
    serializer_class= serializers.TransportationVehicleStateChangeLaneSerializer
    def list(self, request):
        """Forces a lane change to the lane with the given index; if successful,
            the lane will be chosen for the given amount of time (in s)."""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Forces a lane change to the lane with the given index; if successful,the lane will be chosen for the given amount of time (in s).",
                         'vehID': 'Provide a vehicle id',
                         'laneIndex':'Provide the lane Index',
                         'duration':'How long the vehicle will stop',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleStateChangeLaneSerializer(data=request.data)
        if serializer.is_valid():
            vehID = serializer.data.get('vehID')
            laneIndex = serializer.data.get('laneIndex')
            duration = serializer.data.get('duration')
            
            try:
                tracioutput = traci.vehicle.changeLane(vehID, laneIndex, duration)
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)})
            else:
                return Response({'status': 'ok', 'message': "Successful"})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleStateChangeSubLaneViewSet(viewsets.ViewSet):
    """
            Information

           Forces a lateral change by the given amount (negative values indicate changing to the right, positive to the left).
           This will override any other lane change motivations but conform to safety-constraints as configured by laneChangeMode.
        """
    serializer_class= serializers.TransportationVehicleStateChangeSubLaneSerializer
    def list(self, request):
        """Forces a lateral change by the given amount (negative values indicate changing to the right, positive
            to the left). This will override any other lane change motivations but conform to
            safety-constraints as configured by laneChangeMode."""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Forces a lateral change by the given amount (negative values indicate changing to the right, positive to the left). This will override any other lane change motivations but conform to safety-constraints as configured by laneChangeMode.",
                         'vehID': 'Provide a vehicle id',
                         'latDist':'',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleStateChangeSubLaneSerializer(data=request.data)
        if serializer.is_valid():
            vehID = serializer.data.get('vehID')
            latDist = serializer.data.get('latDist')
            
            try:
                tracioutput = traci.vehicle.changeSublane(vehID, latDist)
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)})
            else:
                return Response({'status': 'ok', 'message': "Successful"})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleStateSlowDownViewSet(viewsets.ViewSet):
    """
            Information

          Changes the speed smoothly to the given value over the given amount of time in seconds (can also be used to increase speed).
        """
    serializer_class= serializers.TransportationVehicleStateSlowDownSerializer
    def list(self, request):
        """Changes the speed smoothly to the given value over the given amount
            of time in seconds (can also be used to increase speed)."""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Changes the speed smoothly to the given value over the given amount of time in seconds (can also be used to increase speed).",
                         'vehID': 'Provide a vehicle id',
                         'speed':'Provide the value of the speed',
                         'duration':'Provide the duration in seconds'
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleStateSlowDownSerializer(data=request.data)
        if serializer.is_valid():
            vehID = serializer.data.get('vehID')
            speed = serializer.data.get('speed')
            duration = serializer.data.get('duration')
            
            try:
                tracioutput = traci.vehicle.slowDown(vehID, speed, duration)
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)})
            else:
                return Response({'status': 'ok', 'message': "Successful"})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleStateSetSpeedViewSet(viewsets.ViewSet):
    """
            Information

          Sets the vehicle speed to the given value. The speed will be followed according to the current speed mode.
           By default the vehicle may drive slower than the set speed according to the safety rules of the car-follow model.
           When sending a value of -1 the vehicle will revert to its original behavior (using the maxSpeed of its vehicle type and following all safety rules).
        """
    serializer_class= serializers.TransportationVehicleStateSetSpeedSerializer
    def list(self, request):
        """Sets the speed in m/s for the named vehicle within the last step.
            Calling with speed=-1 hands the vehicle control back to SUMO."""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the speed in m/s for the named vehicle within the last step. Calling with speed=-1 hands the vehicle control back to SUMO.",
                         'vehID': 'Provide a vehicle id',
                         'speed':'Provide the value of the speed',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleStateSetSpeedSerializer(data=request.data)
        if serializer.is_valid():
            vehID = serializer.data.get('vehID')
            speed = serializer.data.get('speed')
            
            try:
                tracioutput = traci.vehicle.setSpeed(vehID, speed)
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)})
            else:
                return Response({'status': 'ok', 'message': "Successful"})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationVehicleStateSetColorViewSet (viewsets.ViewSet):
    """
            Information

          Sets the color for the vehicle with the given ID, i.e. (255,0,0) for the color red.
            The fourth component (alpha) is optional.
        """
    serializer_class = serializers.TransportationVehicleStateSetColorSerializer

    def list (self, request):
        """Sets the color for the vehicle with the given ID, i.e. (255,0,0) for the color red.
            The fourth component (alpha) is optional."""

        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Sets the color for the vehicle with the given ID, i.e. (255,0,0) for the color red."
                                        "The fourth component (alpha) is optional.",
                          'vehID': 'Provide a vehicle id',
                          'color': 'Provide the vehicle color i.e. (255,0,0)',
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleStateSetColorSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            color = serializer.data.get ('color')
            res = eval(color)

            try:
                tracioutput = traci.vehicle.setColor (vehID, res)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})


        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleStatedispatchTaxiViewSet (viewsets.ViewSet):
    """
            Information

         dispatches the taxi with the given id to service the given reservations.
        If only a single reservation is given, this implies pickup and drop-off
        If multiple reservations are given, each reservation id must occur twice
        (once for pickup and once for drop-off) and the list encodes ride
        sharing of passengers (in pickup and drop-off order)
        """
    serializer_class = serializers.TransportationVehicleStateDispatchTaxiSerializer

    def list (self, request):
        """dispatches the taxi with the given id to service the given reservations.
            If only a single reservation is given, this implies pickup and drop-off
            If multiple reservations are given, each reservation id must occur twice
            (once for pickup and once for drop-off) and the list encodes ride
            sharing of passengers (in pickup and drop-off order)"""

        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "dispatches the taxi with the given id to service the given reservations.",
                          'vehID': 'Provide a vehicle id',
                          'color': 'Provide the vehicle color i.e. (255,0,0)',
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleStateDispatchTaxiSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            reservations = serializer.data.get ('reservations')

            try:
                tracioutput = traci.vehicle.dispatchTaxi (vehID, reservations)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})


        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleStateMoveToViewSet(viewsets.ViewSet):
    """
            Information

          Moves the vehicle to a new position along the current route
        """
    serializer_class= serializers.TransportationVehicleStateMoveToSerializer
    def list(self, request):
        """Move a vehicle to a new position along it's current route."""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Move a vehicle to a new position along it's current route.",
                         'vehID': 'Provide a vehicle id',
                         'laneID':'Provide a lane id',
                         'pos':'Provide a position',
                         'reason':'Provide a reason'
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleStateMoveToSerializer(data=request.data)
        if serializer.is_valid():
            vehID = serializer.data.get('vehID')
            laneID = serializer.data.get('laneID')
            pos = serializer.data.get('pos')
            reason = serializer.data.get('reason')
            
            try:
                tracioutput = traci.vehicle.moveTo(vehID, laneID, pos, reason)
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)})
            else:
                return Response({'status': 'ok', 'message': "Successful"})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationVehicleStateMoveToXYViewSet (viewsets.ViewSet):
    """
            Information

            Place vehicle at the given x,y coordinates and force it's angle to
            the given value (for drawing).
            If the angle is set to INVALID_DOUBLE_VALUE, the vehicle assumes the
            natural angle of the edge on which it is driving.
            If keepRoute is set to 1, the closest position
            within the existing route is taken. If keepRoute is set to 0, the vehicle may move to
            any edge in the network but it's route then only consists of that edge.
            If keepRoute is set to 2 the vehicle has all the freedom of keepRoute=0
            but in addition to that may even move outside the road network.
            edgeID and lane are optional placement hints to resolve ambiguities.
            The command fails if no suitable target position is found within the
            distance given by matchThreshold.
        """
    serializer_class = serializers.TransportationVehicleStateMoveToXYSerializer

    def list (self, request):
        """Moves the vehicle to a new position after normal vehicle movements have taken place.
          Also forces the angle of the vehicle to the given value (navigational angle in degree)."""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Moves the vehicle to a new position after normal vehicle movements have taken place."
                            "Also forces the angle of the vehicle to the given value (navigational angle in degree).",
                          'vehID': 'Provide a vehicle id',
                          'edgeID': 'Provide an edge id',
                          'lane': 'Provide a lane id',
                          'x': 'Provide x coordinate',
                          'y': 'Provide y coordinate',
                          'angle': 'Provide the angle',
                          'KeepRoute': '',
                          'matchThreshold':'',
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleStateMoveToXYSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            edgeID = serializer.data.get ('edgeID')
            lane = serializer.data.get ('lane')
            x = serializer.data.get ('x')
            y = serializer.data.get ('y')
            angle = serializer.data.get ('angle')
            keepRoute = serializer.data.get ('keepRoute')
            matchThreshold = serializer.data.get ('matchThreshold')

            try:
                tracioutput = traci.vehicle.moveTo (vehID, edgeID, lane,x,y, angle, keepRoute, matchThreshold)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})


        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleStateReplaceStopViewSet (viewsets.ViewSet):
    """
            Information

            Replaces stop at the given index with a new stop. Automatically modifies
            the route if the replacement stop is at another location.
            For edgeID a stopping place id may be given if the flag marks this
            stop as stopping on busStop, parkingArea, containerStop etc.
            If edgeID is "", the stop at the given index will be removed without
            replacement and the route will not be modified.
            If teleport is set to 1, the route to the replacement stop will be
            disconnected (forcing a teleport).
            If stopIndex is 0 the gap will be between the current
            edge and the new stop. Otherwise the gap will be between the stop edge for
            nextStopIndex - 1 and the new stop.
        """
    serializer_class = serializers.TransportationVehicleStatereplaceStopSerializer

    def list (self, request):
        """Moves the vehicle to a new position after normal vehicle movements have taken place.
          Also forces the angle of the vehicle to the given value (navigational angle in degree)."""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Replaces stop at the given index with a new stop. Automatically modifies the "
                                         "route if the replacement stop is at another location",
                          'vehID': 'Provide a vehicle id',
                          'nextStopIndex': 'Provide next stop Index',
                          'edgeID': 'Provide an edge id',
                          'pos':'Provide a position',
                          'laneIndex': 'Provide a lane index',
                          'duration': 'Provide the duration',
                          'flags': '',
                          'startPos': '',
                          'until': '',
                          'teleport ':'teleport',
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleStatereplaceStopSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            nextStopIndex = serializer.data.get ('nextStopIndex')
            edgeID = serializer.data.get ('edgeID')
            laneIndex = serializer.data.get ('laneIndex')
            pos = serializer.data.get ('pos')
            duration = serializer.data.get ('duration')
            flags = serializer.data.get ('flags')
            startPos = serializer.data.get ('startPos')
            until = serializer.data.get ('until')
            teleport = serializer.data.get('teleport')

            try:
                tracioutput = traci.vehicle.replaceStop (vehID, nextStopIndex, edgeID, pos, laneIndex, duration, flags, startPos, until, teleport)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})


        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class TransportationVehicleStateRerouteTraveltimeViewSet (viewsets.ViewSet):
    """
            Information
            Reroutes a vehicle. If
            currentTravelTimes is True (default) then the current traveltime of the
            edges is loaded and used for rerouting. If currentTravelTimes is False
            custom travel times are used. The various functions and options for
            customizing travel times are described at https://sumo.dlr.de/wiki/Simulation/Routing

            When rerouteTraveltime has been called once with option
            currentTravelTimes=True, all edge weights are set to the current travel
            times at the time of that call (even for subsequent simulation steps).
        """
    serializer_class = serializers.TransportationVehicleStateRerouteTraveltimeSerializer

    def list (self, request):
        """Sets the vehicle's speed mode as a bitset."""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Computes a new route to the current destination that minimizes travel time."
                                         " The assumed values for each edge in the network can be customized in various ways",
                          'vehID': 'Provide a vehicle id',
                          'currentTravelTimes': 'True or False',
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleStateRerouteTraveltimeSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            currentTravelTimes  = serializer.data.get ('currentTravelTimes')

            try:
                tracioutput = traci.vehicle.rerouteTraveltime (vehID, currentTravelTimes)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})


        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleStateRerouteEffortViewSet (viewsets.ViewSet):
    """
            Information
            Computes a new route using the vehicle's internal and the global edge effort information. Replaces the current route by the found
        """
    serializer_class = serializers.TransportationVehicleStateRerouteEffortSerializer

    def list (self, request):
        """Sets the vehicle's speed mode as a bitset."""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Reroutes a vehicle according to the effort values.",
                          'vehID': 'Provide a vehicle id',
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleStateRerouteEffortSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')

            try:
                tracioutput = traci.vehicle.rerouteEffort (vehID)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})

        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class TransportationVehicleStateSetSpeedModeViewSet(viewsets.ViewSet):
    """
            Information

          	Sets how the values set by speed (0x40) and slowdown (0x14) shall be treated. Also allows to configure the behavior at junctions. See below.
        """
    serializer_class= serializers.TransportationVehicleStateSetSpeedModeSerializer
    def list(self, request):
        """Sets the vehicle's speed mode as a bitset."""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the vehicle's speed mode as a bitset.",
                         'vehID': 'Provide a vehicle id',
                         'sm':'Provide the speed mode',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleStateSetSpeedModeSerializer(data=request.data)
        if serializer.is_valid():
            vehID = serializer.data.get('vehID')
            sm = serializer.data.get('sm')
            
            try:
                tracioutput = traci.vehicle.setSpeedMode(vehID, sm)
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)})
            else:
                return Response({'status': 'ok', 'message': "Successful"})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleStateSetSpeedFactorViewSet(viewsets.ViewSet):
    """
            Information

        Sets the vehicle's speed factor to the given value
        """
    serializer_class= serializers.TransportationVehicleStateSetSpeedFactorSerializer
    def list(self, request):
        """Sets the speed factor (tendency to drive faster or slower than)."""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the speed factor (tendency to drive faster or slower than).",
                         'vehID': 'Provide a vehicle id',
                         'factor':'Provide the speed factor',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleStateSetSpeedFactorSerializer(data=request.data)
        if serializer.is_valid():
            vehID = serializer.data.get('vehID')
            factor = serializer.data.get('factor')

            try:
                tracioutput = traci.vehicle.setSpeedFactor (vehID, factor)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})


        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleStateSetMaxSpeedViewSet(viewsets.ViewSet):
    """
            Information

         Sets the vehicle's maximum speed to the given value
        """
    serializer_class= serializers.TransportationVehicleStateSetMaxSpeedSerializer
    def list(self, request):
        """Sets the maximum speed in m/s for this vehicle."""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the maximum speed in m/s for this vehicle.",
                         'vehID': 'Provide a vehicle id',
                         'speed':'Provide the value of the speed',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleStateSetMaxSpeedSerializer(data=request.data)
        if serializer.is_valid():
            vehID = serializer.data.get('vehID')
            speed = serializer.data.get('speed')
            
            try:
                tracioutput = traci.vehicle.setMaxSpeed(vehID, speed)
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)})
            else:
                return Response({'status': 'ok', 'message': "Successful"})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationVehicleStateSetLaneChangeModeViewSet (viewsets.ViewSet):
    """
            Information

         Sets how lane changing in general and lane changing requests by TraCI are performed
        """
    serializer_class = serializers.TransportationVehicleStateSetLaneChangeModeSerializer

    def list (self, request):
        """Sets the maximum speed in m/s for this vehicle."""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Sets the vehicle's lane change mode as a bitset.",
                          'vehID': 'Provide a vehicle id',
                          ' lcm': 'lane change mode',
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleStateSetLaneChangeModeSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            lcm = serializer.data.get ('lcm')

            try:
                tracioutput = traci.vehicle.setLaneChangeMode (vehID, lcm)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})


        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleStateUpdateBestLanesViewSet (viewsets.ViewSet):
    """
            Information

         updates internal data structures for strategic lane choice. (e.g. after modifying access permissions).
         Note: This happens automatically when changing the route or moving to a new edge
        """
    serializer_class = serializers.TransportationVehicleStateUpdateBestLanesSerializer

    def list (self, request):
        """Triggers an update of the vehicle's bestLanes (structure determining the lane preferences used by LC models)
                It may be called after modifying the vClass for instance."""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Triggers an update of the vehicle's bestLanes (structure determining the lane preferences used by LC models)"
                                            "It may be called after modifying the vClass for instance.",
                          'vehID': 'Provide a vehicle id',
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleStateUpdateBestLanesSerializer(data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')

            try:
                tracioutput = traci.vehicle.updateBestLanes (vehID)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})


        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleAddViewSet (viewsets.ViewSet):
    """
            Information
	        Adds the defined vehicle
        """
    serializer_class = serializers.TransportationVehicleAddSerializer

    def list (self, request):
        """	Adds the defined vehicle"""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Add a new vehicle (new style with all possible parameters)",
                          'vehID': 'Provide a vehicle id',
                          'routeID':'Provide a route id',
                          'typeID':'Provide a type id',
                          'depart':'',
                          'departLane':'',
                          'departPos':'',
                          'departSpeed':'',
                          'arrivalLane':'',
                          'arrivalPos':'',
                          'arrivalSpeed':'',
                          'fromTaz':'',
                          'toTaz':'',
                          'line':'',
                          'personCapacity':'',
                          'personNumber':''
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleAddSerializer(data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            routeID = serializer.data.get ('routeID')
            typeID = serializer.data.get ('typeID')
            depart = serializer.data.get ('depart')
            departLane = serializer.data.get ('departLane')
            departPos = serializer.data.get ('departPos')
            departSpeed = serializer.data.get ('departSpeed')
            arrivalLane = serializer.data.get ('arrivalLane')
            arrivalPos = serializer.data.get ('arrivalPos')
            arrivalSpeed = serializer.data.get ('arrivalSpeed')
            fromTaz = serializer.data.get ('fromTaz')
            toTaz = serializer.data.get ('toTaz')
            line = serializer.data.get ('lane')
            personCapacity = serializer.data.get ('personCapacity')
            personNumber = serializer.data.get ('personNumber')

            try:
                tracioutput = traci.vehicle.add (vehID, routeID, typeID, depart, departLane, departPos, departSpeed, arrivalLane, arrivalPos, arrivalSpeed, fromTaz, toTaz,line, personCapacity,personNumber)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})


        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleStateRemoveViewSet(viewsets.ViewSet):
    """
            Information

         Removes the defined vehicle.
        """
    serializer_class= serializers.TransportationVehicleStateRemoveSerializer
    def list(self, request):
        """Remove vehicle with the given ID for the give reason.
            Reasons are defined in module constants and start with REMOVE_"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Remove vehicle with the given ID for the give reason. Reasons are defined in module constants and start with REMOVE_",
                         'vehID': 'Provide a vehicle id',
                         'reason':'Provide the reason',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleStateRemoveSerializer(data=request.data)
        if serializer.is_valid():
            vehID = serializer.data.get('vehID')
            reason = serializer.data.get('reason')
            
            try:
                tracioutput = traci.vehicle.remove(vehID, reason)
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)})
            else:
                return Response({'status': 'ok', 'message': "Successful"})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationVehicleSetLengthViewSet (viewsets.ViewSet):
    """
            Information

         	Sets the vehicle's length to the given value
        """
    serializer_class = serializers.TransportationVehicleSetLengthSerializer

    def list (self, request):
        """Sets the length in m for the given vehicle."""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Sets the length in m for the given vehicle.",
                          'vehID': 'Provide a vehicle id',
                          'length': "Provide the vehicle's length",
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleSetLengthSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            length = serializer.data.get ('length')

            try:
                tracioutput = traci.vehicle.setLength (vehID, length)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})

        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleSetVehicleClassViewSet (viewsets.ViewSet):
    """
            Information
	        Sets the vehicle's length to the given value
        """
    serializer_class = serializers.TransportationVehicleSetVehicleClassSerializer

    def list (self, request):
        """	Sets the vehicle's length to the given value"""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Sets the vehicle's length to the given value",
                          'vehID': 'Provide a vehicle id',
                          'clazz': "Provide the vehicle class",
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleSetVehicleClassSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            clazz = serializer.data.get ('clazz')

            try:
                tracioutput = traci.vehicle.setVehicleClass (vehID, clazz)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})

        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleSetEmissionClassViewSet (viewsets.ViewSet):
    """
            Information
	        .Sets the emission class for this vehicle
        """
    serializer_class = serializers.TransportationVehicleSetEmmisionClassSerializer

    def list (self, request):
        """	Sets the emission class for this vehicle."""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Sets the emission class for this vehicle.",
                          'vehID': 'Provide a vehicle id',
                          'clazz': "Provide the emmision class",
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleSetEmmisionClassSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            clazz = serializer.data.get ('clazz')

            try:
                tracioutput = traci.vehicle.setEmissionClass (vehID, clazz)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})

        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleSetWidthViewSet (viewsets.ViewSet):
    """
            Information
	        Sets the width in m for this vehicle.
        """
    serializer_class = serializers.TransportationVehicleSetWidthSerializer

    def list (self, request):
        """	Sets the width in m for this vehicle."""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Sets the width in m for this vehicle.",
                          'vehID': 'Provide a vehicle id',
                          'width': "Provide the vehicle width",
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleSetWidthSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            width = serializer.data.get ('width')

            try:
                tracioutput = traci.vehicle.setWidth (vehID, width)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})

        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleSetHeightViewSet (viewsets.ViewSet):
    """
            Information
	        Sets the height in m for this vehicle.
        """
    serializer_class = serializers.TransportationVehicleSetHeightSerializer

    def list (self, request):
        """	Sets the height in m for this vehicle."""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Sets the height in m for this vehicle.",
                          'vehID': 'Provide a vehicle id',
                          'height': "Provide the vehicle height",
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleSetHeightSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            height = serializer.data.get ('height')

            try:
                tracioutput = traci.vehicle.setHeight (vehID, height)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})

        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleMinGapViewSet (viewsets.ViewSet):
    """
            Information
	        Sets the vehicle's minimum headway gap to the given value
        """
    serializer_class = serializers.TransportationVehicleSetMinGapSerializer

    def list (self, request):
        """	Sets the offset (gap to front vehicle if halting) for this vehicle."""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Sets the offset (gap to front vehicle if halting) for this vehicle.",
                          'vehID': 'Provide a vehicle id',
                          'minGap': "Provide the min Gap",
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleSetMinGapSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            minGap = serializer.data.get ('minGap')

            try:
                tracioutput = traci.vehicle.setMinGap (vehID, minGap)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})

        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleSetShapeClassViewSet (viewsets.ViewSet):
    """
            Information
	        Sets the vehicle's shape class to the given value
        """
    serializer_class = serializers.TransportationVehicleSetShapeClassSerializer

    def list (self, request):
        """Sets the shape class for this vehicle."""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Sets the shape class for this vehicle.",
                          'vehID': 'Provide a vehicle id',
                          'clazz': "Provide the vehicle's shape class",
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleSetShapeClassSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            clazz = serializer.data.get ('clazz')

            try:
                tracioutput = traci.vehicle.setShapeClass (vehID,clazz)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})

        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleSetAccelerationViewSet (viewsets.ViewSet):
    """
            Information
	        Sets the vehicle's wished maximum acceleration to the given value
        """
    serializer_class = serializers.TransportationVehicleSetAccelerationSerializer

    def list (self, request):
        """Sets the vehicle's wished maximum acceleration to the given value"""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Sets the vehicle's wished maximum acceleration to the given value	",
                          'vehID': 'Provide a vehicle id',
                          'accel': "Provide the vehicle's maximum acceleration",
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleSetAccelerationSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            accel = serializer.data.get ('accel')

            try:
                tracioutput = traci.vehicle.setAccel (vehID,accel)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})

        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleSetDecelerationViewSet (viewsets.ViewSet):
    """
            Information
            Sets the vehicle's wished maximum deceleration to the given value"""
    serializer_class = serializers.TransportationVehicleSetDecelerationSerializer

    def list (self, request):
        """Sets the preferred maximal deceleration in m/s^2 for this vehicle."""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Sets the preferred maximal deceleration in m/s^2 for this vehicle.",
                          'vehID': 'Provide a vehicle id',
                          'decel': "Provide the vehicle's maximum deceleration",
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleSetDecelerationSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            decel = serializer.data.get ('decel')

            try:
                tracioutput = traci.vehicle.setDecel (vehID,decel)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})

        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleSetImperfectionViewSet (viewsets.ViewSet):
    """
            Information
            Sets the vehicle's driver imperfection (sigma) to the given value	"""
    serializer_class = serializers.TransportationVehicleSetImperfectionSerializer

    def list (self, request):
        """Sets the preferred maximal deceleration in m/s^2 for this vehicle."""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Sets the vehicle's driver imperfection (sigma) to the given value	",
                          'vehID': 'Provide a vehicle id',
                          'imperfection': "Provide the vehicle's driver imperfection",
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleSetImperfectionSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            imperfection = serializer.data.get ('imperfection')

            try:
                tracioutput = traci.vehicle.setImperfection (vehID,imperfection)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})

        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleSetTauViewSet (viewsets.ViewSet):
    """
            Information
            Sets the vehicle's wished headway time to the given value."""
    serializer_class = serializers.TransportationVehicleSetTauctionSerializer

    def list (self, request):
        """Sets the driver's tau-parameter (reaction time or anticipation time depending on the car-following model) in s
            for this vehicle."""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Sets the driver's tau-parameter (reaction time or anticipation time depending on the car-following model) in s for this vehicle.",
                          'vehID': 'Provide a vehicle id',
                          'tau': "Provide the driver's tau-parameter",
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleSetTauctionSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            tau = serializer.data.get ('tau')

            try:
                tracioutput = traci.vehicle.setTau (vehID,tau)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})

        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleSetTypeViewSet (viewsets.ViewSet):
    """
            Information
            Sets the id of the type for the named vehicle."""
    serializer_class = serializers.TransportationVehicleSetTypeSerializer

    def list (self, request):
        """Sets the id of the type for the named vehicle."""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Sets the id of the type for the named vehicle.",
                          'vehID': 'Provide a vehicle id',
                          'typeID': "Provide the typeID",
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleSetTypeSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            typeID = serializer.data.get ('typeID')

            try:
                tracioutput = traci.vehicle.setType (vehID,typeID)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})

        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleSetViaViewSet (viewsets.ViewSet):
    """
            Information
            Changes the via edges to the given edges list (to be used during subsequent rerouting calls)."""
    serializer_class = serializers.TransportationVehicleSetViaSerializer

    def list (self, request):
        """changes the via edges to the given edges list (to be used during
            subsequent rerouting calls).
            Note: a single edgeId as argument is allowed as shorthand for a list of length 1"""

        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Changes the via edges to the given edges list (to be used during subsequent rerouting calls).",
                          'vehID': 'Provide a vehicle id',
                          'list': "Provide the edges list",
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleSetViaSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            list = serializer.data.get ('list')

            try:
                tracioutput = traci.vehicle.setVia (vehID,list)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})

        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleSetMaxSpeedLatViewSet (viewsets.ViewSet):
    """
            Information
            Sets the maximum lateral speed in m/s for this vehicle.	"""
    serializer_class = serializers.TransportationVehicleSetMaxSpeedLatSerializer

    def list (self, request):
        """Sets the maximum lateral speed in m/s for this vehicle."""

        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Sets the maximum lateral speed in m/s for this vehicle.",
                          'vehID': 'Provide a vehicle id',
                          'speed': "Provide maximum lateral speed in m/s",
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleSetMaxSpeedLatSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            speed = serializer.data.get ('speed')

            try:
                tracioutput = traci.vehicle.setMaxSpeedLat (vehID,speed)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})

        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleSetMinGapLatViewSet (viewsets.ViewSet):
    """
            Information
            Sets the minimum lateral gap of the vehicle at 50km/h in m"""
    serializer_class = serializers.TransportationVehicleSetMinGapSerializer

    def list (self, request):
        """Sets the minimum lateral gap of the vehicle at 50km/h in m"""

        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Sets the minimum lateral gap of the vehicle at 50km/h in m",
                          'vehID': 'Provide a vehicle id',
                          'minGapLat': "Provide the minimum lateral gap in m/s",
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleSetMinGapSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            MinGapLat = serializer.data.get ('MinGapLat')

            try:
                tracioutput = traci.vehicle.setMinGapLat (vehID,MinGapLat)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})

        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleSetLateralAlignmentViewSet (viewsets.ViewSet):
    """
            Information
            Sets the preferred lateral alignment for this vehicle."""
    serializer_class = serializers.TransportationVehicleSetLateralAlignmentSerializer

    def list (self, request):
        """"""

        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Sets the preferred lateral alignment for this vehicle.",
                          'vehID': 'Provide a vehicle id',
                          'align': "Provide the lateral alignment for this vehicle",
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleSetLateralAlignmentSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            align = serializer.data.get ('align')

            try:
                tracioutput = traci.vehicle.setLateralAlignment (vehID,align)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})

        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleSetParameterViewSet (viewsets.ViewSet):
    """
            Information
            Sets the preferred lateral alignment for this vehicle."""
    serializer_class = serializers.TransportationVehicleSetParameterSerializer

    def list (self, request):
        """"""

        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Sets the preferred lateral alignment for this vehicle.",
                          'vehID': 'Provide a vehicle id',
                          'align': "Provide the lateral alignment for this vehicle",
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleSetParameterSerializer (data = request.data)
        if serializer.is_valid ():
            objID = serializer.data.get ('objID')
            param = serializer.data.get ('param')
            value = serializer.data.get('value')

            try:
                tracioutput = traci.vehicle.setParameter (objID,param,value)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})

        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationVehicleSetActionStepLengthViewSet (viewsets.ViewSet):
    """
            Information
            Sets the current action step length for the vehicle in s. If the boolean value resetActionOffset is true, an action step is scheduled immediately for the vehicle."""
    serializer_class = serializers.TransportationVehiclesetActionStepLengthSerializer

    def list (self, request):
        """
        Sets the action step length for this vehicle. If resetActionOffset == True (default), the
        next action point is scheduled immediately. if If resetActionOffset == False, the interval
        between the last and the next action point is updated to match the given value, or if the latter
        is smaller than the time since the last action point, the next action follows immediately.
        """

        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Sets the preferred lateral alignment for this vehicle.",
                          'vehID': 'Provide a vehicle id',
                          'actionStepLength': "Provide the lateral alignment for this vehicle",
                          'resetActionOffset':'',
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehiclesetActionStepLengthSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            actionStepLength = serializer.data.get ('actionStepLength')
            resetActionOffset = serializer.data.get('resetActionOffset')

            try:
                tracioutput = traci.vehicle.setParameter (vehID,actionStepLength,resetActionOffset)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})

        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationRouteGetIDListViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get a list of all routes in the network
    """
    def list(self, request):
        """Returns a list of all objects in the network"""
        try:
            traciout = traci.route.getIDList ()
        except Exception as e:
            return Response ({'status': 'error', 'message': str (e)})
        else:
            return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns a list of all routes in the network.",
                         'data':traciout
                         }
                        )



class TransportationRouteGetIDCountViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get the number of all routes in the network
    """
    def list(self, request):
        """Returns a list of all objects in the network"""
        try:
            traciout = traci.route.getIDCount()
        except Exception as e:
            return Response ({'status': 'error', 'message': str (e)})
        else:
            return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns the number of all routes in the network.",
                         'data':traciout
                         }
                        )



class TransportationRouteGetEdgesViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to get a list of all edges in the route.
    """
    serializer_class = serializers.TransportationRouteGetSerializer
    def list(self, request):
        """Returns a list of Water Start Features"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Returns a list of all edges in the route.",
                         'routeID': 'Provide a route id',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationRouteGetSerializer(data=request.data)
        if serializer.is_valid():
            routeID = serializer.data.get('routeID')
            
            try:
                tracioutput = traci.route.getEdges(routeID)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'data': tracioutput})

                
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationRouteAddViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to add a new route with the given id consisting of the given list of edge IDs.
    """
    serializer_class = serializers.TransportationRouteAddSerializer
    def list(self, request):
        """Returns a list of Water Start Features"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Adds a new route with the given id consisting of the given list of edge IDs.",
                         'routeID': 'Provide a route id',
                         'edges': 'provide a list of edge IDs.',
                         'edges_example': ['edge_1', 'edge_2']
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationRouteAddSerializer(data=request.data)
        if serializer.is_valid():
            routeID = serializer.data.get('routeID')
            edges = serializer.data.get('edges')
            if "(" not in edges or ")" not in edges:
                return Response({'status': 'error', 'message': 'edges must be tuble','edges_example': ('class_1', 'class_2')})
            else:
                
                try:
                    new_edges = ast.literal_eval(edges)
                except:
                    
                    return Response ({'status': 'Error', 'message': 'Give a tuple as in the example format', 'edges_example': ('class_1', 'class_2')})
                try:
                    traciout = traci.route.add(routeID,new_edges)
                except Exception as e:
                    return Response ({'status': 'Error', 'message': str (e)})
                else:
                    return Response ({'status': 'ok', 'message': routeID + " " + str(new_edges)})

                    
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationLaneSetAllowedViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to set a list of allowed vehicle classes.
        Use the 'laneID' field, to provide the lane id.
        Use the 'allowedClasses' field, to provide a list of allowed vehicle classes.
    """
    serializer_class = serializers.TransportationLaneSetAllowedSerializer
    def list(self, request):
        """Returns a list of Water Start Features"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets a list of allowed vehicle classes.",
                         'laneID': 'provide the lane id',
                         'allowedClasses': 'provide a list of allowed vehicle classes, or leave empty which means means all vehicles are allowed',
                         'allowedClasses_example': ["class_1", "class_2"]
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationLaneSetAllowedSerializer(data=request.data)
        if serializer.is_valid():
            laneID = serializer.data.get('laneID')
            allowedClasses = serializer.data.get('allowedClasses')
            # aclasses = allowedClasses.strip('][').split(', ')


            if "[" not in allowedClasses or "]" not in allowedClasses:
                return Response({'status': 'error', 'message': 'allowedClasses must be a list'})
            else:
                
                try:
                    aclasses = ast.literal_eval (allowedClasses)
                except:
                    
                    return Response ({'status': 'Error', 'message': 'Give a list as in the example format', 'disallowedClasses_example': ['class_1', 'class_2']})
                try:
                    traci.lane.setAllowed(laneID,aclasses)
                except Exception as e:
                    return Response ({'status': 'Error', 'message': str (e)})
                else:
                    return Response ({'status': 'ok', 'laneID': laneID, 'allowedClasses': allowedClasses})

                    
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationLaneSetDisallowedViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to set a list of disallowed vehicle classes.
        Use the 'laneID' field, to provide the lane id.
        Use the 'disallowedClasses' field, to provide a list of disallowed vehicle classes.
    """
    serializer_class = serializers.TransportationLaneSetDisallowedSerializer
    def list(self, request):
        """"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets a list of disallowed vehicle classes.",
                         'laneID': 'provide the lane id',
                         'disallowedClasses': 'provide a list of disallowed vehicle classes, or leave empty which means means all vehicles are not allowed',
                         'disallowedClasses_example': ['class_1', 'class_2']
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationLaneSetDisallowedSerializer(data=request.data)
        if serializer.is_valid():
            laneID = serializer.data.get('laneID')
            disallowedClasses = serializer.data.get('disallowedClasses')
            # dclasses = disallowedClasses.strip ('][').split (', ')
            if "[" not in disallowedClasses or "]" not in disallowedClasses:
                return Response({'status': 'error', 'message': 'disallowedClasses must be a list'})
            else:
                
                try:
                    dclasses = ast.literal_eval (disallowedClasses)
                except:
                    return Response ({'status': 'Error', 'message': 'Give a list as in the example format', 'disallowedClasses_example': ['class_1', 'class_2'] })
                try:
                    traci.lane.setDisallowed (laneID, dclasses)
                except Exception as e:
                    return Response ({'status': 'Error', 'message': str (e)})
                else:
                    return Response ({'status': 'ok', 'laneID': laneID, 'disallowedClasses': dclasses})

                    
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationLaneSetLengthViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to set the length of the lane.
    """
    serializer_class = serializers.TransportationLaneSetLengthSerializer
    def list(self, request):
        """"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the length of the lane in m.",
                         'laneID': 'provide the lane id',
                         'length': 'provide the lane length',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationLaneSetLengthSerializer(data=request.data)
        if serializer.is_valid():
            laneID = serializer.data.get('laneID')
            length = serializer.data.get('length')
            try:
                traciout = traci.lane.setLength(laneID,length)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': laneID + " " + str(length)})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationLaneSetMaxSpeedViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to set a new maximum allowed speed on the lane in m/s.
    """
    serializer_class = serializers.TransportationLaneSetMaxSpeedSerializer
    def list(self, request):
        """"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets a new maximum allowed speed on the lane in m/s.",
                         'laneID': 'provide the lane id',
                         'speed': 'provide a maximum allowed speed on the lane in m/s',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationLaneSetMaxSpeedSerializer(data=request.data)
        if serializer.is_valid():
            laneID = serializer.data.get('laneID')
            speed = serializer.data.get('speed')
            try:
                traciout = traci.lane.setMaxSpeed (laneID, speed)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': laneID + " " + str(speed)})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationPersonAddViewSet(viewsets.ViewSet):
    """
        Information
        Inserts a new person to the simulation at the given edge, position and time (in s).
        This function should be followed by appending Stages or the person will immediately vanish on departure.
    """
    serializer_class = serializers.TransportationPersonAddSerializer
    def list(self, request):
        """
        Inserts a new person to the simulation at the given edge, position and
        time (in s). This function should be followed by appending Stages or the person
        will immediately vanish on departure.
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Inserts a new person to the simulation at the given edge, position and"
                            "time (in s). This function should be followed by appending Stages or the person"
                            "will immediately vanish on departure.",
                         'PersonID': 'provide the person id',
                         'edgeId': 'provide the edge id',
                         'pos':'',
                         'depart':'',
                         'typeID':'',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationPersonAddSerializer(data=request.data)
        if serializer.is_valid():
            personID = serializer.data.get('personID')
            edgeID = serializer.data.get('edgeID')
            pos = serializer.data.get('pos')
            depart = serializer.data.get('depart')
            typeID = serializer.data.get('typeID')
            try:
                traciout = traci.person.add (personID,edgeID,pos,depart,typeID)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationPersonAppendDrivingStageViewSet(viewsets.ViewSet):
    """
        Information
        Appends a driving stage to the plan of the given person
        The lines parameter should be a space-separated list of line ids
    """
    serializer_class = serializers.TransportationPersonAppendDrivingStageSerializer
    def list(self, request):
        """
        Appends a driving stage to the plan of the given person
        The lines parameter should be a space-separated list of line ids
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Appends a driving stage to the plan of the given person"
                                        "The lines parameter should be a space-separated list of line ids",
                         'PersonID': 'provide the person id',
                         'toEdge': 'provide the edge id',
                         'lines':'',
                         'stopID':'',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationPersonAppendDrivingStageSerializer(data=request.data)
        if serializer.is_valid():
            personID = serializer.data.get('personID')
            toEdge = serializer.data.get('toEdge')
            lines = serializer.data.get('lines')
            stopID = serializer.data.get('stopID')
            try:
                traciout = traci.person.appendDrivingStage (personID,toEdge,lines,stopID)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationPersonAppendWaitingStageViewSet(viewsets.ViewSet):
    """
        Information
        Appends a waiting stage with duration in s to the plan of the given person

    """
    serializer_class = serializers.TransportationPersonAppendWaitingStageSerializer
    def list(self, request):
        """
        Appends a waiting stage with duration in s to the plan of the given person

        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Appends a waiting stage with duration in s to the plan of the given person",
                         'PersonID': 'provide the person id',
                         'duration': '',
                         'description':'',
                         'stopID':'',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationPersonAppendWaitingStageSerializer(data=request.data)
        if serializer.is_valid():
            personID = serializer.data.get('personID')
            duration = serializer.data.get('duration')
            description = serializer.data.get('description')
            stopID = serializer.data.get('stopID')
            try:
                traciout = traci.person.appendWaitingStage (personID,duration,description,stopID)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationPersonAppendWalkingStageViewSet (viewsets.ViewSet):
    """
        Information
        Appends a walking stage to the plan of the given person
        The walking speed can either be specified, computed from the duration parameter (in s) or taken from the
        type of the person
    """
    serializer_class = serializers.TransportationPersonAppendWalkingStageSerializer

    def list (self, request):
        """"""
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Appends a walking stage to the plan of the given person"
                                        "The walking speed can either be specified, computed from the duration parameter (in s) or taken from the"
                                        "type of the person.",
                          'personID': 'provide a person id',
                          'edges': ['edge_1', 'edge_2'],
                          'arrivalPos': '',
                          'duration':'',
                          'speed':'',
                          'stopID':'',
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationPersonAppendWalkingStageSerializer(data = request.data)
        if serializer.is_valid ():
            personID = serializer.data.get ('personID')
            edges = serializer.data.get ('edges')
            arrivalPos = serializer.data.get('arrivalPos')
            duration = serializer.data.get('duration')
            speed = serializer.data.get('speed')
            stopID = serializer.data.get('stopID')
            if "[" not in edges or "]" not in edges:
                return Response ({'status': 'error', 'message': 'disallowedClasses must be a list'})
            else:

                try:
                    dclasses = ast.literal_eval (edges)
                except:
                    return Response ({'status': 'Error', 'message': 'Give a list as in the example format',
                                      'edges': ['edges_1', 'edges_2']})
                try:
                    traci.person.appendWalkingStage (personID, edges, arrivalPos,duration,speed,stopID)
                except Exception as e:
                    return Response ({'status': 'Error', 'message': str (e)})
                else:
                    return Response ({'status': 'ok', 'message': 'successful'})

        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationPersonRemoveStageViewSet(viewsets.ViewSet):
    """
        Information
       Removes the nth next stage
        nextStageIndex must be lower then value of getRemainingStages(personID)
        nextStageIndex 0 immediately aborts the current stage and proceeds to the next stage
    """
    serializer_class = serializers.TransportationPersonRemoveStageSerializer
    def list(self, request):
        """
       Removes the nth next stage
        nextStageIndex must be lower then value of getRemainingStages(personID)
        nextStageIndex 0 immediately aborts the current stage and proceeds to the next stage

        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Removes the nth next stage",
                         'PersonID': 'provide the person id',
                         'nextStageIndex': '',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationPersonRemoveStageSerializer(data=request.data)
        if serializer.is_valid():
            personID = serializer.data.get('personID')
            nextStageIndex = serializer.data.get('nextStageIndex')
            try:
                traciout = traci.person.removeStage (personID,nextStageIndex)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationPersonRemoveStagesViewSet(viewsets.ViewSet):
    """
        Information
        Removes all stages of the person. If no new phases are appended,
        the person will be removed from the simulation in the next simulationStep().
    """
    serializer_class = serializers.TransportationPersonRemoveStageSerializer
    def list(self, request):
        """
       Removes all stages of the person. If no new phases are appended,
        the person will be removed from the simulation in the next simulationStep().

        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Removes all stages of the person.",
                         'PersonID': 'provide the person id',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationPersonRemoveStagesSerializer(data=request.data)
        if serializer.is_valid():
            personID = serializer.data.get('personID')
            try:
                traciout = traci.person.removeStages (personID)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationPersonRerouteTraveltimeViewSet(viewsets.ViewSet):
    """
        Information
        Computes a new route to the current destination that minimizes travel time.
         The assumed values for each edge in the network can be customized in various ways.
    """
    serializer_class = serializers.TransportationPersonRerouteTraveltimeSerializer
    def list(self, request):
        """
        Computes a new route to the current destination that minimizes travel time.
         The assumed values for each edge in the network can be customized in various ways.

        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Computes a new route to the current destination that minimizes travel time",
                         'PersonID': 'provide the person id',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationPersonRerouteTraveltimeSerializer(data=request.data)
        if serializer.is_valid():
            personID = serializer.data.get('personID')
            try:
                traciout = traci.person.rerouteTraveltime (personID)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationPersonMoveToXYViewSet(viewsets.ViewSet):
    """
        Information
        Place person at the given x,y coordinates and force it's angle to
        the given value (for drawing).
        If the angle is set to INVALID_DOUBLE_VALUE, the vehicle assumes the
        natural angle of the edge on which it is driving.
        If keepRoute is set to 1, the closest position
        within the existing route is taken. If keepRoute is set to 0, the vehicle may move to
        any edge in the network but it's route then only consists of that edge.
        If keepRoute is set to 2 the person has all the freedom of keepRoute=0
        but in addition to that may even move outside the road network.
        edgeID is an optional placement hint to resolve ambiguities.
        The command fails if no suitable target position is found within the
        distance given by matchThreshold.
    """
    serializer_class = serializers.TransportationPersonMoveToXYSerializer
    def list(self, request):
        """
        Place person at the given x,y coordinates and force it's angle to
        the given value (for drawing).
        If the angle is set to INVALID_DOUBLE_VALUE, the vehicle assumes the
        natural angle of the edge on which it is driving.
        If keepRoute is set to 1, the closest position
        within the existing route is taken. If keepRoute is set to 0, the vehicle may move to
        any edge in the network but it's route then only consists of that edge.
        If keepRoute is set to 2 the person has all the freedom of keepRoute=0
        but in addition to that may even move outside the road network.
        edgeID is an optional placement hint to resolve ambiguities.
        The command fails if no suitable target position is found within the
        distance given by matchThreshold.

        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Moves the person to a new position after normal movements have taken place."
                                        " Also forces the angle of the person to the given value (navigational angle in degree).",
                         'PersonID': 'provide the person id',
                         'edgeID':'provide the edge id',
                         'x':'provide the x position',
                         'y':'provide the y position',
                         'angle':'',
                         'keepRoute':'',
                         'matchThreshold':''
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationPersonMoveToXYSerializer(data=request.data)
        if serializer.is_valid():
            personID = serializer.data.get('personID')
            edgeID = serializer.data.get('edgeID')
            x = serializer.data.get('x')
            y = serializer.data.get('y')
            angle = serializer.data.get('angle')
            keepRoute = serializer.data.get('keepRoute')
            matchThreshold = serializer.data.get('matchThreshold')


            try:
                traciout = traci.person.moveToXY (personID, edgeID, x, y, angle, keepRoute, matchThreshold)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationPersonSetHeightViewSet(viewsets.ViewSet):
    """
        Information
        Sets the height in m for this person.
    """
    serializer_class = serializers.TransportationPersonSetHeightSerializer
    def list(self, request):
        """
        Sets the height in m for this person.
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the height in m for this person.",
                         'PersonID': 'provide the person id',
                         'height':'provide the height in m',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationPersonSetHeightSerializer(data=request.data)
        if serializer.is_valid():
            personID = serializer.data.get('personID')
            height = serializer.data.get('height')

            try:
                traciout = traci.person.setHeight(personID, height)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationPersonSetLengthViewSet(viewsets.ViewSet):
    """
        Information
        Sets the length in m for the given person.
    """
    serializer_class = serializers.TransportationPersonSetLengthSerializer
    def list(self, request):
        """
        Sets the length in m for the given person.
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the length in m for the given person.",
                         'PersonID': 'provide the person id',
                         'length':'provide the length in m',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationPersonSetLengthSerializer(data=request.data)
        if serializer.is_valid():
            personID = serializer.data.get('personID')
            length = serializer.data.get('length')

            try:
                traciout = traci.person.setLength(personID, length)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationPersonSetMinGapViewSet(viewsets.ViewSet):
    """
        Information
        Sets the offset (gap to front person if halting) for this vehicle.
    """
    serializer_class = serializers.TransportationPersonSetMinGapSerializer
    def list(self, request):
        """
        Sets the offset (gap to front person if halting) for this vehicle.
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the offset (gap to front person if halting) for this vehicle.",
                         'PersonID': 'provide the person id',
                         'minGap':'provide the gap to front person if halting',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationPersonSetMinGapSerializer(data=request.data)
        if serializer.is_valid():
            personID = serializer.data.get('personID')
            minGap = serializer.data.get('minGap')

            try:
                traciout = traci.person.setMinGap(personID, minGap)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationPersonSetSpeedViewSet(viewsets.ViewSet):
    """
        Information
        Sets the maximum speed in m/s for the named person for subsequent step.
    """
    serializer_class = serializers.TransportationPersonSetSpeedSerializer
    def list(self, request):
        """
        Sets the maximum speed in m/s for the named person for subsequent step.
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the maximum speed in m/s for the named person for subsequent step.",
                         'PersonID': 'provide the person id',
                         'speed':'provide the maximum speed in m/s ',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationPersonSetSpeedSerializer(data=request.data)
        if serializer.is_valid():
            personID = serializer.data.get('personID')
            speed = serializer.data.get('speed')

            try:
                traciout = traci.person.setSpeed(personID, speed)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationPersonSetTypeViewSet(viewsets.ViewSet):
    """
        Information
        Sets the id of the type for the named person.
    """
    serializer_class = serializers.TransportationPersonSetTypeSerializer
    def list(self, request):
        """
        Sets the id of the type for the named person.
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the id of the type for the named person.",
                         'PersonID': 'provide the person id',
                         'typeID':'provide the id of the type',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationPersonSetTypeSerializer(data=request.data)
        if serializer.is_valid():
            personID = serializer.data.get('personID')
            typeID = serializer.data.get('typeID')

            try:
                traciout = traci.person.setType(personID, typeID)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationPersonSetWidthViewSet(viewsets.ViewSet):
    """
        Information
        Sets the width in m for this person.
    """
    serializer_class = serializers.TransportationPersonSetWidthSerializer
    def list(self, request):
        """
        Sets the width in m for this person.
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the width in m for this person.",
                         'PersonID': 'provide the person id',
                         'width':'provide the width in m',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationPersonSetWidthSerializer(data=request.data)
        if serializer.is_valid():
            personID = serializer.data.get('personID')
            width = serializer.data.get('width')

            try:
                traciout = traci.person.setWidth(personID, width)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationPersonSetColorViewSet (viewsets.ViewSet):
    """
            Information

          Sets the color for the vehicle with the given ID, i.e. (255,0,0) for the color red.
            The fourth component (alpha) is optional.
        """
    serializer_class = serializers.TransportationPersonSetColorSerializer

    def list (self, request):
        """Sets the color for the vehicle with the given ID, i.e. (255,0,0) for the color red.
            The fourth component (alpha) is optional."""

        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Sets the color for the vehicle with the given ID, i.e. (255,0,0) for the color red."
                                        "The fourth component (alpha) is optional.",
                          'personID': 'Provide a person id',
                          'color': 'Provide the vehicle color i.e. (255,0,0)',
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationPersonSetColorSerializer (data = request.data)
        if serializer.is_valid ():
            personID = serializer.data.get ('personID')
            color = serializer.data.get ('color')
            res = eval(color)

            try:
                tracioutput = traci.person.setColor (personID, res)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})


        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)



class TransportationVehicleTypeSetLengthViewSet(viewsets.ViewSet):
    """
        Information
       Sets the length in m of the vehicles of this type.
    """
    serializer_class = serializers.TransportationVehicleTypeSetLengthSerializer
    def list(self, request):
        """
        Sets the length in m of the vehicles of this type.
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the length in m of the vehicles of this type.",
                         'typeID': "provide the vehicle's type",
                         'length':'provide the length in m',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleTypeSetLengthSerializer(data=request.data)
        if serializer.is_valid():
            typeID = serializer.data.get('typeID')
            length = serializer.data.get('length')

            try:
                traciout = traci.vehicletype.setLength(typeID, length)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleTypeSetMaxSpeedViewSet(viewsets.ViewSet):
    """
        Information
        Sets the maximum speed in m/s of vehicles of this type.
    """
    serializer_class = serializers.TransportationVehicleTypeSetMaxSpeedSerializer
    def list(self, request):
        """
        Sets the maximum speed in m/s of vehicles of this type.
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the maximum speed in m/s of vehicles of this type.",
                         'typeID': "provide the vehicle's type",
                         'speed':'provide speed in m/s',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleTypeSetMaxSpeedSerializer(data=request.data)
        if serializer.is_valid():
            typeID = serializer.data.get('typeID')
            speed = serializer.data.get('speed')

            try:
                traciout = traci.vehicletype.setMaxSpeed(typeID, speed)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleTypeSetVehicleClassViewSet(viewsets.ViewSet):
    """
        Information
        Sets the class of vehicles of this type.
    """
    serializer_class = serializers.TransportationVehicleTypeSetVehicleClassSerializer
    def list(self, request):
        """
        Sets the class of vehicles of this type.
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the class of vehicles of this type.",
                         'typeID': "provide the vehicle's type",
                         'clazz':'provide the class',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleTypeSetVehicleClassSerializer(data=request.data)
        if serializer.is_valid():
            typeID = serializer.data.get('typeID')
            clazz = serializer.data.get('clazz')

            try:
                traciout = traci.vehicletype.setVehicleClass(typeID, clazz)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleTypeSetSpeedFactorViewSet(viewsets.ViewSet):
    """
        Information
        Sets the speed factor of vehicles of this type.
    """
    serializer_class = serializers.TransportationVehicleTypeSetSpeedFactorSerializer
    def list(self, request):
        """
        Sets the speed factor of vehicles of this type.
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the speed factor of vehicles of this type.",
                         'typeID': "provide the vehicle's type",
                         'factor':'provide the speed factor',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleTypeSetSpeedFactorSerializer(data=request.data)
        if serializer.is_valid():
            typeID = serializer.data.get('typeID')
            factor = serializer.data.get('factor')

            try:
                traciout = traci.vehicletype.setSpeedFactor(typeID, factor)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleTypeSetSpeedDeviationViewSet(viewsets.ViewSet):
    """
        Information
        Sets the maximum speed deviation of vehicles of this type.
    """
    serializer_class = serializers.TransportationVehicleTypeSetSpeedDeviationSerializer
    def list(self, request):
        """
        Sets the maximum speed deviation of vehicles of this type.
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the maximum speed deviation of vehicles of this type.",
                         'typeID': "provide the vehicle's type",
                         'deviation':'provide the speed deviation',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleTypeSetSpeedDeviationSerializer(data=request.data)
        if serializer.is_valid():
            typeID = serializer.data.get('typeID')
            deviation = serializer.data.get('deviation')

            try:
                traciout = traci.vehicletype.setSpeedDeviation(typeID, deviation)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleTypeSetEmissionClassViewSet(viewsets.ViewSet):
    """
        Information
        Sets the emission class of vehicles of this type.
    """
    serializer_class = serializers.TransportationVehicleTypeSetEmissionClassSerializer
    def list(self, request):
        """
       Sets the emission class of vehicles of this type.
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the emission class of vehicles of this type.",
                         'typeID': "provide the vehicle's type",
                         'clazz':'provide the emission class',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleTypeSetEmissionClassSerializer(data=request.data)
        if serializer.is_valid():
            typeID = serializer.data.get('typeID')
            clazz = serializer.data.get('clazz')

            try:
                traciout = traci.vehicletype.setEmissionClass(typeID, clazz)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleTypeSetWidthViewSet(viewsets.ViewSet):
    """
        Information
       Sets the width in m of vehicles of this type.
    """
    serializer_class = serializers.TransportationVehicleTypeSetWidthSerializer
    def list(self, request):
        """
       Sets the width in m of vehicles of this type.
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the width in m of vehicles of this type.",
                         'typeID': "provide the vehicle's type",
                         'width':'provide the width in m',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleTypeSetWidthSerializer(data=request.data)
        if serializer.is_valid():
            typeID = serializer.data.get('typeID')
            width = serializer.data.get('width')

            try:
                traciout = traci.vehicletype.setWidth(typeID, width)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleTypeSetHeightViewSet(viewsets.ViewSet):
    """
        Information
       Sets the height in m of vehicles of this type.
    """
    serializer_class = serializers.TransportationVehicleTypeSetHeightSerializer
    def list(self, request):
        """
       Sets the height in m of vehicles of this type.
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the height in m of vehicles of this type.",
                         'typeID': "provide the vehicle's type",
                         'height':'provide the height in m',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleTypeSetHeightSerializer(data=request.data)
        if serializer.is_valid():
            typeID = serializer.data.get('typeID')
            height = serializer.data.get('height')

            try:
                traciout = traci.vehicletype.setHeight(typeID, height)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleTypeSetMinGapViewSet(viewsets.ViewSet):
    """
        Information
       Sets the offset (gap to front vehicle if halting) of vehicles of this type.
    """
    serializer_class = serializers.TransportationVehicleTypeSetMinGapSerializer
    def list(self, request):
        """
       Sets the offset (gap to front vehicle if halting) of vehicles of this type.
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the offset (gap to front vehicle if halting) of vehicles of this type.",
                         'typeID': "provide the vehicle's type",
                         'minGap':'provide the gap to front vehicle if halting',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleTypeSetMinGapSerializer(data=request.data)
        if serializer.is_valid():
            typeID = serializer.data.get('typeID')
            minGap = serializer.data.get('minGap')

            try:
                traciout = traci.vehicletype.setMinGap(typeID, minGap)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleTypeSetShapeClassViewSet(viewsets.ViewSet):
    """
        Information
        Sets the shape class of vehicles of this type.
    """
    serializer_class = serializers.TransportationVehicleTypeSetShapeClassSerializer
    def list(self, request):
        """
       Sets the shape class of vehicles of this type.
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the shape class of vehicles of this type.",
                         'typeID': "provide the vehicle's type",
                         'clazz':'provide the shape class',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleTypeSetShapeClassSerializer(data=request.data)
        if serializer.is_valid():
            typeID = serializer.data.get('typeID')
            clazz = serializer.data.get('clazz')

            try:
                traciout = traci.vehicletype.setShapeClass(typeID, clazz)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleTypeSetAccelerationViewSet(viewsets.ViewSet):
    """
        Information
        Sets the maximum acceleration in m/s^2 of vehicles of this type.
    """
    serializer_class = serializers.TransportationVehicleTypeSetShapeClassSerializer
    def list(self, request):
        """
       Sets the maximum acceleration in m/s^2 of vehicles of this type.
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the maximum acceleration in m/s^2 of vehicles of this type.",
                         'typeID': "provide the vehicle's type",
                         'accel':'provide the maximum acceleration',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleTypeSetAccelerationSerializer(data=request.data)
        if serializer.is_valid():
            typeID = serializer.data.get('typeID')
            accel = serializer.data.get('accel')

            try:
                traciout = traci.vehicletype.setAccel(typeID, accel)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleTypeSetDecelerationViewSet(viewsets.ViewSet):
    """
        Information
        Sets the maximal comfortable deceleration in m/s^2 of vehicles of this type.
    """
    serializer_class = serializers.TransportationVehicleTypeSetDecelerationSerializer
    def list(self, request):
        """
       Sets the maximal comfortable deceleration in m/s^2 of vehicles of this type.
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the maximal comfortable deceleration in m/s^2 of vehicles of this type.",
                         'typeID': "provide the vehicle's type",
                         'decel':'provide the maximum deceleration',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleTypeSetDecelerationSerializer(data=request.data)
        if serializer.is_valid():
            typeID = serializer.data.get('typeID')
            decel = serializer.data.get('decel')

            try:
                traciout = traci.vehicletype.setDecel(typeID, decel)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleTypeSetImperfectionViewSet(viewsets.ViewSet):
    """
        Information
        Sets the driver imperfection of vehicles of this type.
    """
    serializer_class = serializers.TransportationVehicleTypeSetImperfectionSerializer
    def list(self, request):
        """
       Sets the driver imperfection of vehicles of this type.
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the driver imperfection of vehicles of this type.",
                         'typeID': "provide the vehicle's type",
                         'imperfection':'provide the driver imperfection',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleTypeSetImperfectionSerializer(data=request.data)
        if serializer.is_valid():
            typeID = serializer.data.get('typeID')
            imperfection = serializer.data.get('imperfection')

            try:
                traciout = traci.vehicletype.setImperfection(typeID, imperfection)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleTypeSetTauViewSet(viewsets.ViewSet):
    """
        Information
        Sets the driver's tau-parameter (reaction time or anticipation time depending on the car-following model) in s
        for vehicles of this type.
    """
    serializer_class = serializers.TransportationVehicleTypeSetTauSerializer
    def list(self, request):
        """
       Sets the driver's tau-parameter (reaction time or anticipation time depending on the car-following model) in s
        for vehicles of this type.
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the driver's tau-parameter (reaction time or anticipation time depending on the car-following model) in s"
                                        "for vehicles of this type.",
                         'typeID': "provide the vehicle's type",
                         'tau':"provide the driver's tau-parameter",
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleTypeSetTauSerializer(data=request.data)
        if serializer.is_valid():
            typeID = serializer.data.get('typeID')
            tau = serializer.data.get('tau')

            try:
                traciout = traci.vehicletype.setTau(typeID, tau)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleTypeSetMaxSpeedLatViewSet(viewsets.ViewSet):
    """
        Information
        Sets the maximum lateral speed of this type.
    """
    serializer_class = serializers.TransportationVehicleTypeSetMaxSpeedLatSerializer
    def list(self, request):
        """
       Sets the maximum lateral speed of this type.
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the maximum lateral speed of this type.",
                         'typeID': "provide the vehicle's type",
                         'speed':"provide the  maximum lateral speed ",
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleTypeSetMaxSpeedLatSerializer(data=request.data)
        if serializer.is_valid():
            typeID = serializer.data.get('typeID')
            speed = serializer.data.get('speed')

            try:
                traciout = traci.vehicletype.setMaxSpeedLat(typeID, speed)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleTypeSetMinGapLatViewSet(viewsets.ViewSet):
    """
        Information
        Sets the minimum lateral gap at 50km/h of this type.
    """
    serializer_class = serializers.TransportationVehicleTypeSetMinGapLatSerializer
    def list(self, request):
        """
       Sets the minimum lateral gap at 50km/h of this type.
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the minimum lateral gap at 50km/h of this type.",
                         'typeID': "provide the vehicle's type",
                         'minGapLat':"provide the  minimum lateral gap ",
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleTypeSetMinGapLatSerializer(data=request.data)
        if serializer.is_valid():
            typeID = serializer.data.get('typeID')
            minGapLat = serializer.data.get('minGapLat')

            try:
                traciout = traci.vehicletype.setMinGapLat(typeID, minGapLat)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleTypeSetLateralAlignmentViewSet(viewsets.ViewSet):
    """
        Information
        Sets the preferred lateral alignment of this type.
    """
    serializer_class = serializers.TransportationVehicleTypeSetLateralAlignmentSerializer
    def list(self, request):
        """
       Sets the preferred lateral alignment of this type.
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the preferred lateral alignment of this type.",
                         'typeID': "provide the vehicle's type",
                         'latAlignment':"provide the preferred lateral alignment ",
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleTypeSetLateralAlignmentSerializer(data=request.data)
        if serializer.is_valid():
            typeID = serializer.data.get('typeID')
            latAlignment = serializer.data.get('latAlignment')

            try:
                traciout = traci.vehicletype.setLateralAlignment(typeID, latAlignment)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleTypeCopyViewSet(viewsets.ViewSet):
    """
        Information
        Duplicates the vType with ID origTypeID. The newly created vType is assigned the ID newTypeID
    """
    serializer_class = serializers.TransportationVehicleTypeCopySerializer
    def list(self, request):
        """
       Duplicates the vType with ID origTypeID. The newly created vType is assigned the ID newTypeID
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Duplicates the vType with ID origTypeID. The newly created vType is assigned the ID newTypeID.",
                         'origTypeID': "provide the vType",
                         'newTypeID':"provide the new vType ",
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleTypeCopySerializer(data=request.data)
        if serializer.is_valid():
            origTypeID = serializer.data.get('origTypeID')
            newTypeID = serializer.data.get('newTypeID')

            try:
                traciout = traci.vehicletype.copy(origTypeID, newTypeID)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleTypeActionStepLengthViewSet(viewsets.ViewSet):
    """
        Information
        Sets the action step length for this vehicle. If resetActionOffset == True (default), the
        next action point is scheduled immediately. if If resetActionOffset == False, the interval
        between the last and the next action point is updated to match the given value, or if the latter
        is smaller than the time since the last action point, the next action follows immediately.
    """
    serializer_class = serializers.TransportationVehicleTypeSetActionStepLengthSerializer
    def list(self, request):
        """
       Sets the action step length for this vehicle. If resetActionOffset == True (default), the
        next action point is scheduled immediately. if If resetActionOffset == False, the interval
        between the last and the next action point is updated to match the given value, or if the latter
        is smaller than the time since the last action point, the next action follows immediately.
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the current action step length for the vehicle type in s."
                                        " If the boolean value resetActionOffset is true, an action step is scheduled immediately for all vehicles of the type.",
                         'vehID': "provide the vehicle id",
                         'actionStepLength':"",
                         'resetActionOffset': "",
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationVehicleTypeSetActionStepLengthSerializer
        if serializer.is_valid():
            vehID = serializer.data.get('vehID')
            actionStepLength = serializer.data.get('actionStepLength')
            resetActionOffset = serializer.data.get('resetActionOffset')

            try:
                traciout = traci.vehicletype.setActionStepLength(vehID, actionStepLength,resetActionOffset)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationVehicleTypeSetColorViewSet (viewsets.ViewSet):
    """
            Information
            Sets the color of this type.

        """
    serializer_class = serializers.TransportationVehicleTypeSetColorSerializer

    def list (self, request):
        """Sets the color of this type."""

        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Sets the color of this type.",
                          'personID': 'Provide a person id',
                          'color': 'Provide the vehicle color i.e. (255,0,0)',
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationVehicleTypeSetColorSerializer (data = request.data)
        if serializer.is_valid ():
            vehID = serializer.data.get ('vehID')
            color = serializer.data.get ('color')
            res = eval(color)

            try:
                tracioutput = traci.vehicletype.setColor (vehID, res)
            except Exception as e:
                return Response ({'status': 'error', 'message': str (e)})
            else:
                return Response ({'status': 'ok', 'message': "Successful"})


        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationRouteAddViewSet (viewsets.ViewSet):
    """
        Information
        Adds a new route with the given id consisting of the given list of edge IDs.
    """
    serializer_class = serializers.TransportationRouteAddSerializer

    def list (self, request):
        """
        Adds a new route with the given id consisting of the given list of edge IDs.
        """
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Adds a new route with the given id consisting of the given list of edge IDs.",
                          'routeID': 'Provide a route id',
                          'edges': 'provide a list of edges',
                          'edges_example': ['1', '2', '4', '6', '7']
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationRouteAddSerializer (data = request.data)
        if serializer.is_valid ():
            routeID = serializer.data.get ('routeID')
            edges = serializer.data.get ('edges')
            # dclasses = disallowedClasses.strip ('][').split (', ')
            if "[" not in edges or "]" not in edges:
                return Response ({'status': 'error', 'message': 'edges must be a list'})
            else:
                try:
                    dclasses = ast.literal_eval (edges)
                except:
                    return Response ({'status': 'Error', 'message': 'Give a list as in the example format',
                                      'edges_example': ['1', '2', '4', '6', '7']})
                try:
                    traci.vehicle.add (routeID, dclasses)
                except Exception as e:
                    return Response ({'status': 'Error', 'message': str (e)})
                else:
                    return Response ({'status': 'ok', 'message': 'successful'})


        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TransportationPoIStateSetTypeViewSet(viewsets.ViewSet):
    """
        Information
        Sets the (abstract) type of the poi.
    """
    serializer_class = serializers.TransportationPoIStateSetTypeSerializer
    def list(self, request):
        """
       Sets the (abstract) type of the poi.
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the (abstract) type of the poi.",
                         'poiID': "provide the poi id",
                         'poiType':"Provide the poi type",
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationPoIStateSetTypeSerializer(data = request.data)
        if serializer.is_valid():
            poiID = serializer.data.get('poiID')
            poiType = serializer.data.get('poiType')

            try:
                traciout = traci.poi.setType(poiID, poiType)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationPoIStateSetPositionViewSet(viewsets.ViewSet):
    """
        Information
        Sets the position coordinates of the poi.

    """
    serializer_class = serializers.TransportationPoIStateSetPositionSerializer
    def list(self, request):
        """
       Sets the position coordinates of the poi.

        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Sets the position coordinates of the poi.",
                         'poiID': "Provide the poi id",
                         'x': "provide the poi x position",
                         'y':"Provide the poi y position",
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationPoIStateSetPositionSerializer(data = request.data)
        if serializer.is_valid():
            poiID = serializer.data.get('poiID')
            x = serializer.data.get('x')
            y = serializer.data.get('y')
            pos = (x,y)

            try:
                traciout = traci.poi.setPosition(poiID, pos)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationPoIStateSetWidthViewSet(viewsets.ViewSet):
    """
        Information
        Sets the width of the poi.

    """
    serializer_class = serializers.TransportationPoIStateSetWidthSerializer
    def list(self, request):
        """
        Sets the width of the poi.

        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information':'Sets the width of the poi.',
                         'poiID': "Provide the poi id",
                         'width': "provide the poi's width",
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationPoIStateSetWidthSerializer(data = request.data)
        if serializer.is_valid():
            poiID = serializer.data.get('poiID')
            width = serializer.data.get('width')

            try:
                traciout = traci.poi.setWidth(poiID, width)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationPoIStateSetHeightViewSet(viewsets.ViewSet):
    """
        Information
        Sets the height of the poi.

    """
    serializer_class = serializers.TransportationPoIStateSetHeightSerializer
    def list(self, request):
        """
        Sets the height of the poi.

        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information':'Sets the height of the poi.',
                         'poiID': "Provide the poi id",
                         'height': "provide the poi's width",
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationPoIStateSetHeightSerializer(data = request.data)
        if serializer.is_valid():
            poiID = serializer.data.get('poiID')
            height = serializer.data.get('height')

            try:
                traciout = traci.poi.setHeight(poiID, height)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationPoIStateSetAngleViewSet(viewsets.ViewSet):
    """
        Information
        Sets the angle of the poi.

    """
    serializer_class = serializers.TransportationPoIStateSetAngleSerializer
    def list(self, request):
        """
        Sets the angle of the poi.

        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information':'Sets the angle of the poi.',
                         'poiID': "Provide the poi id",
                         'height': "provide the poi's width",
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationPoIStateSetAngleSerializer(data = request.data)
        if serializer.is_valid():
            poiID = serializer.data.get('poiID')
            angle = serializer.data.get('angle')

            try:
                traciout = traci.poi.setAngle(poiID, angle)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationPoIStateRemoveViewSet(viewsets.ViewSet):
    """
        Information
        Removes the poi with the given poiID


    """
    serializer_class = serializers.TransportationPoIStateRemoveSerializer
    def list(self, request):
        """
        Removes the poi with the given poiID

        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information':'Removes the poi with the given poiID',
                         'poiID': "Provide the poi id",
                         'layer': "provide the layer",
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationPoIStateRemoveSerializer(data = request.data)
        if serializer.is_valid():
            poiID = serializer.data.get('poiID')
            layer = serializer.data.get('layer')

            try:
                traciout = traci.poi.remove(poiID, layer)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationPolygonSetTypeViewSet(viewsets.ViewSet):
    """
        Information
        Sets the (abstract) type of the polygon.

    """
    serializer_class = serializers.TransportationPolygonSetTypeSerializer
    def list(self, request):
        """
        Sets the (abstract) type of the polygon.

        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information':'Sets the (abstract) type of the polygon.',
                         'polygonID': "Provide the polygon id",
                         'polygonType': "provide the polygon type",
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationPolygonSetTypeSerializer(data = request.data)
        if serializer.is_valid():
            polygonID = serializer.data.get('polygonID')
            polygonType = serializer.data.get('polygonType')

            try:
                traciout = traci.polygon.setType(polygonID, polygonType)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationPolygonSetFilledViewSet(viewsets.ViewSet):
    """
        Information
        Sets the filled status of the polygon

    """
    serializer_class = serializers.TransportationPolygonSetFilledSerializer
    def list(self, request):
        """
        Sets the filled status of the polygon

        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information':'Sets the filled status of the polygon',
                         'polygonID': "Provide the polygon id",
                         'filled': "provide the filled status",
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationPolygonSetFilledSerializer(data = request.data)
        if serializer.is_valid():
            polygonID = serializer.data.get('polygonID')
            filled = serializer.data.get('filled')

            try:
                traciout = traci.polygon.setFilled(polygonID, filled)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationPolygonSetLineWidthViewSet(viewsets.ViewSet):
    """
        Information
       Sets the line width for drawing unfilled polygon

    """
    serializer_class = serializers.TransportationPolygonSetLineWidthSerializer
    def list(self, request):
        """
       Sets the line width for drawing unfilled polygon

        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information':'Sets the line width for drawing unfilled polygon',
                         'polygonID': "Provide the polygon id",
                         'lineWidth': "provide the line width",
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationPolygonSetLineWidthSerializer(data = request.data)
        if serializer.is_valid():
            polygonID = serializer.data.get('polygonID')
            lineWidth = serializer.data.get('lineWidth')

            try:
                traciout = traci.polygon.setFilled(polygonID, lineWidth)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationPolygonRemoveViewSet(viewsets.ViewSet):
    """
        Information
       Removes a polygon with the given ID

    """
    serializer_class = serializers.TransportationPolygonRemoveSerializer
    def list(self, request):
        """
       Removes a polygon with the given ID

        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information':'Removes a polygon with the given ID',
                         'polygonID': "Provide the polygon id",
                         'layer': "provide the layer",
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationPolygonRemoveSerializer(data = request.data)
        if serializer.is_valid():
            polygonID = serializer.data.get('polygonID')
            layer = serializer.data.get('layer')

            try:
                traciout = traci.polygon.remove(polygonID, layer)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#TODO
class TransportationPolygonAddDynamicsViewSet (viewsets.ViewSet):
    """
        Information
        Adds the specified dynamics for the Polygon
    """
    serializer_class = serializers.TransportationPolygonAddDynamicsSerializer

    def list (self, request):
        """
        Adds the specified dynamics for the Polygon
        """
        return Response ({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                          'information': "Adds the specified dynamics for the Polygon",
                          'polygonID': 'ID of the polygon, upon which the specified dynamics shall act',
                          'trackedObjectID':'ID of a SUMO traffic object, which shall be tracked by the polygon',
                          'timeSpan': "list of time points for timing the animation keyframes (must start with element zero)"
                                        "If it has length zero, no animation is taken into account.",
                          'timeSpan_example': ['1', '2', '4', '6', '7'],
                          'alphaSpan':"list of alpha values to be attained at keyframes intermediate values are"
                                        "obtained by linear interpolation. Must have length equal to timeSpan, or zero"
                                        "if no alpha animation is desired.",
                          'alphaSpan_example': ['1', '2', '4', '6', '7'],
                          'looped':" Whether the animation should restart when the last keyframe is reached. In that case"
                                    "the animation jumps to the first keyframe as soon as the last is reached."
                                    "If looped==false, the controlled polygon is removed as soon as the timeSpan elapses.",
                          'rotate': "Whether, the polygon should be rotated with the tracked object (only applies when such is given)"
                                    "The center of rotation is the object's position."
                          }
                         )

    def post (self, request):
        """"""
        serializer = serializers.TransportationPolygonAddDynamicsSerializer (data = request.data)
        if serializer.is_valid ():
            polygonID = serializer.data.get ('routeID')
            trackedObjectID = serializer.data.get('trackedObjectID')
            timeSpan = serializer.data.get ('timeSpan')
            alphaSpan = serializer.data.get('alphaSpan')
            looped = serializer.data.get('looped')
            rotate = serializer.data.get('rotate')
            dclasses = timeSpan.strip ('][').split (', ')
            print(dclasses)
            if "[" not in timeSpan or "]" not in timeSpan:
                return Response ({'status': 'error', 'message': 'timeSpan must be a list'})
            else:
                try:
                    tclasses = []
                    for element in timeSpan:
                        tclasses.append (float (element))
                    print(tclasses)
                except:
                    return Response ({'status': 'Error', 'message': 'Give a list as in the example format',
                                      'timespan_example': ['1', '2', '4', '6', '7']})
            if "[" not in alphaSpan or "]" not in alphaSpan:
                return Response ({'status': 'error', 'message': 'timeSpan must be a list'})
            else:
                try:
                    aclasses = []
                    for element in alphaSpan:
                        aclasses.append (float (element))
                    print(aclasses)
                except:
                    return Response ({'status': 'Error', 'message': 'Give a list as in the example format',
                                      'alphaspan_example': ['1', '2', '4', '6', '7']})
                try:
                    traci.polygon.addDynamics (polygonID, trackedObjectID, tclasses, aclasses, looped, rotate)
                except Exception as e:
                    return Response ({'status': 'Error', 'message': str (e)})
                else:
                    return Response ({'status': 'ok', 'message': 'successful'})

        else:
            return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class TransportationEdgesAdaptTraveltimeViewSet(viewsets.ViewSet):
    """
        Information
      Adapt the travel time value (in s) used for (re-)routing for the given edge.

        When setting begin time and end time (in seconds), the changes only
        apply to that time range. Otherwise they apply all the time

    """
    serializer_class = serializers.TransportationEdgesAdaptTraveltimeSerializer
    def list(self, request):
        """
       Adapt the travel time value (in s) used for (re-)routing for the given edge.

        When setting begin time and end time (in seconds), the changes only
        apply to that time range. Otherwise they apply all the time

        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information':'Adapt the travel time value (in s) used for (re-)routing for the given edge.',
                         'edgeID': "Provide the polygon id",
                         'time': "provide the travel time",
                         'begin': "provide the begin time",
                         'end': "provide the end time",

                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationEdgesAdaptTraveltimeSerializer(data = request.data)
        if serializer.is_valid():
            edgeID = serializer.data.get('edgeID')
            time = serializer.data.get('time')
            begin = serializer.data.get('begin')
            end = serializer.data.get('end')


            try:
                traciout = traci.edge.adaptTraveltime(edgeID, time, begin, end)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationEdgesSetEffortViewSet(viewsets.ViewSet):
    """
        Information
        Adapt the effort value used for (re-)routing for the given edge.

        When setting begin time and end time (in seconds), the changes only
        apply to that time range. Otherwise they apply all the time

    """
    serializer_class = serializers.TransportationEdgesSetEffortSerializer
    def list(self, request):
        """
        Adapt the effort value used for (re-)routing for the given edge.

        When setting begin time and end time (in seconds), the changes only
        apply to that time range. Otherwise they apply all the time

        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information':'Adapt the effort value used for (re-)routing for the given edge.',
                         'edgeID': "Provide the polygon id",
                         'effort': "provide the effort value",
                         'begin': "provide the begin time",
                         'end': "provide the end time",

                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationEdgesSetEffortSerializer(data = request.data)
        if serializer.is_valid():
            edgeID = serializer.data.get('edgeID')
            effort = serializer.data.get('effort')
            begin = serializer.data.get('begin')
            end = serializer.data.get('end')


            try:
                traciout = traci.edge.setEffort(edgeID, effort, begin, end)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationEdgesSetMaxSpeedViewSet(viewsets.ViewSet):
    """
        Information
        Set a new maximum speed (in m/s) for all lanes of the edge.

    """
    serializer_class = serializers.TransportationEdgesSetMaxSpeedSerializer
    def list(self, request):
        """
        Set a new maximum speed (in m/s) for all lanes of the edge.

        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information':'Set a new maximum speed (in m/s) for all lanes of the edge.',
                         'edgeID': "Provide the edge id",
                         'speed': "provide the maximum speed",

                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationEdgesSetMaxSpeedSerializer(data = request.data)
        print(serializer)
        if serializer.is_valid():
            edgeID = serializer.data.get('edgeID')
            speed = serializer.data.get('speed')

            try:
                traciout = traci.edge.setMaxSpeed(edgeID, speed)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#TODO
class TransportationSimulationClearPendingViewSet(viewsets.ViewSet):
    """
        Information
        Set a new maximum speed (in m/s) for all lanes of the edge.

    """
    serializer_class = serializers.TransportationSimulationClearPendingSerializer
    def list(self, request):
        """
        Set a new maximum speed (in m/s) for all lanes of the edge.

        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information':'Set a new maximum speed (in m/s) for all lanes of the edge.',
                         'edgeID': "Provide the edge id",
                         'speed': "provide the maximum speed",

                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationSimulationClearPendingSerializer(data = request.data)
        if serializer.is_valid():
            routeID = serializer.data.get('routeID')

            try:
                traciout = traci.simulation.clearPending(routeID)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationSimulationSaveStateViewSet(viewsets.ViewSet):
    """
        Information
        Saves current simulation state to the given filename.

    """
    serializer_class = serializers.TransportationSimulationSaveStateSerializer
    def list(self, request):
        """
            Saves current simulation state to the given filename.
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information':'Saves current simulation state to the given filename.',
                         'fileName': "Provide the file name",

                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationSimulationSaveStateSerializer(data = request.data)
        if serializer.is_valid():
            fileName = serializer.data.get('fileName')

            try:
                traciout = traci.simulation.saveState(fileName)
                print(traciout)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': traciout})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransportationSimulationLoadStateViewSet(viewsets.ViewSet):
    """
        Information
        Saves current simulation state to the given filename.

    """
    serializer_class = serializers.TransportationSimulationLoadStateSerializer
    def list(self, request):
        """
            Saves current simulation state to the given filename.
        """
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information':'Saves current simulation state to the given filename.',
                         'fileName': "Provide the file name",

                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationSimulationLoadStateSerializer(data = request.data)
        if serializer.is_valid():
            fileName = serializer.data.get('fileName')

            try:
                traciout = traci.simulation.loadState(fileName)
            except Exception as e:
                return Response ({'status': 'Error', 'message': str (e)})
            else:
                return Response({'status': 'ok', 'message': 'successful'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransportationStartViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to start Sumo simulation.
    """
    def list(self, request):
        """"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Start Sumo simulation",

                         }
                        )
    def post(self, request):
        """"""
        import os, sys
        if 'SUMO_HOME' in os.environ:
            tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
            sys.path.append(tools)
        else:
            tools = os.path.join("/usr/bin/sumo/", 'tools')
            sys.path.append(tools)

        sumoBinary = "/usr/bin/sumo"

        # import traci as tr
        # import sumolib.miscutils

        try:
            traci.close()
        except Exception as e:
            None
            # return Response({'status': 'error', 'message': str(e)})

        print("start")
        # PORT = sumolib.miscutils.getFreeSocketPort()
        global port
        # port = PORT
        # print("port", PORT)
        sumoCmd = [sumoBinary, "-c", "limassol/lim.sumocfg"]
        print("next")
        traci.start(sumoCmd)
        print("end")
        return Response({'status': 'ok', 'message': "Successful"})


class TransportationStepsViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint to move forward the simulation.
    """
    serializer_class = serializers.TransportationStepSerializer
    def list(self, request):
        """"""
        return Response({'Title': 'KIOS BaSP REST API for Transportation Simulations',
                         'information': "Move simulation time",
                         'steps': 'Provide the number of steps',
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.TransportationStepSerializer(data=request.data)
        if serializer.is_valid():
            steps = serializer.data.get('steps')
            traci.simulationStep(steps)
            return Response({'status': 'ok', 'message': "Successful"})

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Power
class PowerViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint for power.
    """
    serializer_class = serializers.PowerSerializer
    def list(self, request):
        """"""
        return Response({'Title': 'KIOS BaSP REST API for Power Simulations',
                         'Experiment Name': 'Provide an experiment name',
                         'Timestep': 'Provide the time step',
                         'Itterations': 'Provide the number of iterations'
                         }
                        )
    def post(self, request):
        """"""
        serializer = serializers.PowerSerializer(data=request.data)
        if serializer.is_valid():
            timestep = serializer.data.get('timestep')
            itterations = serializer.data.get('itterations')
            experiment_name = serializer.data.get('experiment_name')
            if timestep > 0 and itterations > 0 and len(experiment_name)>0:
                rcommand = "cd /mcr-install; bash run.sh "+str(timestep)+" "+str(itterations)
                host = 'matlab'
                username = 'root'
                password = 'matlab'
                con = paramiko.SSHClient()
                con.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
                con.connect(host, username=username, password=password)
                stdin, stdout, stderr = con.exec_command(rcommand)
                finalfilename = "results-"+str(timestep)+"-"+str(itterations)+".mat"
                dlocation = '/usr/src/app/basp/uploads/'+experiment_name
                if not os.path.exists(dlocation):
                    os.makedirs(dlocation)
                if stderr.read() == b'':
                    for line in stdout.readlines():
                        print(line.strip())
                else:
                    print(stderr.read())
                givenfile = False
                try:
                    scp = SCPClient(con.get_transport())
                    scp.get('/mcr-install/results.mat')
                    givenfile = True
                except:
                    givenfile = False
                if givenfile:
                    filelocation = '/usr/src/app/results.mat'
                    newlocation = '/usr/src/app/basp/uploads/'+experiment_name+'/'+finalfilename
                    os.rename(filelocation, newlocation)
                newlocationurl = "http://localhost:8000/basp/uploads/"+experiment_name+'/'+finalfilename
                finalmessage = "Download simulator data at: "+str(newlocationurl)
                return Response({'status': 'ok', 'message': finalmessage})
            else:
                return Response ({'status': 'error', 'message': 'timestep and itterations must be positive integer'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# CIS
class CISStartViewSet(viewsets.ViewSet):
    """
        Information

        Use this API endpoint for power.
    """
    serializer_class = serializers.CISStartSerializer
    def list(self, request):
        """
        Information
        Use this API endpoint to run CIS simulations using Water, Transportation and Power simulators.
    """
        existing_ex_names = list(models.ExperimentNames.objects.all())
        allthenames = []
        for value in existing_ex_names:
            allthenames.append(value.ex_name)
        return Response(status=status.HTTP_200_OK, data={'Title': 'KIOS BaSP REST API for Simultaneous Water/Transoportation/Power Simulations',
                                                         'information': 'Here you can start a multi-simulator simulation',
                                                         'details': 'the values in the reserved list are not allowed as experiment names',
                                                         'reserved_list': allthenames,
                                                         'Experiment Name*': 'Provide an experiment name',
                                                         'Start Date': 'Provide the start date',
                                                         'Timestep Size Water': 'Provide the time step size for Water Simulations (seconds)',
                                                         'Timestep Size Transportation': 'Provide the time step size for Transportation Simulations (seconds)',
                                                         'Timestep Size Power': 'Provide the time step size for Power Simulations (seconds)',
                                                         'Itterations': 'Provide the number of iterations',
                                                         'Events': 'Provide the events yml file',
                                                         'Sensors': 'Provide the sensors yml file'
                                                         })
    def post(self, request):
        from datetime import timedelta
        """"""
        serializer = serializers.CISStartSerializer(data=request.data)
        if serializer.is_valid():
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            experiment_name = serializer.data.get('experiment_name')
            start_date = serializer.data.get('start_date')
            timestep_size_water = serializer.data.get('timestep_size_water')
            timestep_size_transportation = serializer.data.get('timestep_size_transportation')
            timestep_size_power = serializer.data.get('timestep_size_power')
            itterations = serializer.data.get('itterations')
            events = serializer.data.get('events')
            water_sensors = serializer.data.get('water_sensors')
            existing_ex_names = list(models.ExperimentNames.objects.all())
            allthenames = []
            for value in existing_ex_names:
                allthenames.append(value.ex_name)
            if experiment_name not in allthenames:
                if timestep_size_water > 0 and timestep_size_transportation > 0 and timestep_size_power > 0 and itterations > 0 and len(experiment_name)>0:
                    sensors = re.sub(r"[\n\t]*", "", water_sensors)
                    if events is not None:
                        print('adding events')
                    final_sensors_json_file_contents = ""
                    fs = FileSystemStorage()
                    sensors = ContentFile(sensors)
                    filename = fs.save(experiment_name + '/test.json', sensors)
                    f = default_storage.open(os.path.join(filename), 'r')
                    with f as json_file:
                        final_sensors_json_file_contents = json.load(json_file)
                    startdate_object = datetime.strptime(start_date, '%Y-%m-%d')
                    timedurationinseconds = int(timestep_size_water) * int(itterations)
                    enddate_object = startdate_object + timedelta(seconds=timedurationinseconds)
                    datediff = enddate_object - startdate_object
                    days, seconds = datediff.days, datediff.total_seconds()
                    hours = days * 24
                    epoch1 = datetime.utcfromtimestamp(0)
                    startdate_epoch = (startdate_object - epoch1).total_seconds() * 1000.0
                    enddate_epoch = (enddate_object - epoch1).total_seconds() * 1000.0
                    if enddate_epoch < startdate_epoch:
                        return Response(status=status.HTTP_400_BAD_REQUEST,
                                        data={'start_date': startdate_epoch, 'end_date': enddate_epoch,
                                              'message': 'startdate>enddate'})
                    else:
                        #try:
                        # Water Simulation
                        # Get Report Timestep
                        opts = wn.options
                        #wn.options.time.report_timestep = str(timestep_size_water)

                        # print(timestepinseconds)
                        # Put New Duration
                        wn.options.time.duration = int(seconds)
                        wn.write_inpfile('basp/Water/Water.inp')
                        # Run EPANET & Convert Bin to JSON wntr
                        watersim.wntr2jsonwntr(wn, 'basp/Water/jsonoutput.json')
                        # Write EPANET JSON to PostgreSQL
                        print('000000000000000000000000')
                        watersim.readjsonwithfiles('basp/Water/jsonoutput.json', startdate_object,
                                                   timestep_size_water, final_sensors_json_file_contents, experiment_name)
                        print('111111111111111111111111111111111')
                        # Save Experiment Name in the database
                        newname = models.ExperimentNames(ex_name=experiment_name,
                                                         ex_sensor_filename=str(filename))
                        newname.save()
                        return Response(status=status.HTTP_200_OK, data={'startdate': start_date, 'message': 'simulation completed'})
                        '''
                        except:
                            return Response(status=status.HTTP_400_BAD_REQUEST,
                                            data={'startdate': startdate_epoch, 'enddate': enddate_epoch,
                                                  'message': 'simulation not completed'})
                        '''
                    data = {'message': 'all good'}
                    return Response(status=status.HTTP_200_OK,data=data)
                else:
                    data = {'message': 'Timestep size and itterations must be a positive integer'}
                    return Response(status=status.HTTP_400_BAD_REQUEST, data=data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'experimentname is reserved'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WaterStartWntrView(viewsets.ViewSet):
    """
        Information
        Use this API endpoint to run an EPANET simulation.
        Values in the database will be used to create the EPANET inp file.
        You can provide details such as start/end date.
    """
    serializer_class = serializers.WaterStartSerializerWNTR
    def list(self, request):
        """Returns a list of Water Start Features"""
        existing_ex_names = list(models.ExperimentNames.objects.all())
        allthenames = []
        for value in existing_ex_names:
            allthenames.append(value.ex_name)
        return Response(status=status.HTTP_200_OK, data={'Title': 'KIOS BaSP REST API for Water Simulations',
                         'information': 'Here you can start a WNTR simulation',
                         'details': 'the values in the reserved list are not allowed as experiment names',
                         'reserved_list': allthenames})

    def post(self, request):
        """"""
        #start_time = time.time()
        serializer = serializers.WaterStartSerializerWNTR(data=request.data)
        if serializer.is_valid():
            inp_file = 'basp/Water/Water.inp'
            wn = wntr.network.WaterNetworkModel(inp_file)
            startdate = serializer.data.get('startdate')
            enddate = serializer.data.get('enddate')
            existing_ex_names = list(models.ExperimentNames.objects.all())
            allthenames = []
            for value in existing_ex_names:
                allthenames.append(value.ex_name)
            experimentname = serializer.data.get('experimentname')
            if experimentname not in allthenames:
                sensors = serializer.data.get('sensors')
                sensors = re.sub(r"[\n\t]*", "", sensors)
                fileleak = request.data.get('leakages')
                if fileleak is not None:
                    if len(fileleak) > 0:
                        try:
                            #inp_file = 'basp/Water/Water.inp'
                            #wn = wntr.network.WaterNetworkModel(inp_file)
                            wn = addleakages.addwaterleak(fileleak, wn)
                            #wn.write_inpfile('basp/Water/Water.inp')
                        except:
                            return Response(status=status.HTTP_400_BAD_REQUEST,data={'error': 'leakages file issue'})
                final_sensors_json_file_contents = ""
                fs = FileSystemStorage()
                sensors = ContentFile(sensors)
                filename = fs.save(experimentname+'/test.json', sensors)
                f = default_storage.open(os.path.join(filename), 'r')
                with f as json_file:
                    final_sensors_json_file_contents = json.load(json_file)
                startdate_object = datetime.strptime(startdate, '%Y-%m-%d')
                enddate_object = datetime.strptime(enddate, '%Y-%m-%d')
                datediff = enddate_object - startdate_object
                days, seconds = datediff.days, datediff.total_seconds()
                hours = days * 24
                epoch1 = datetime.utcfromtimestamp(0)
                startdate_epoch = (startdate_object - epoch1).total_seconds() * 1000.0
                enddate_epoch = (enddate_object - epoch1).total_seconds() * 1000.0
                grafanaurl = "http://localhost:3001/d/GIfxrnEGz/water-sensors-basp?orgId=1&from="+str(int(startdate_epoch))+"&to="+str(int(enddate_epoch))
                if hours < 1:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={'startdate': startdate, 'enddate': enddate, 'message': 'startdate>enddate'})
                else:
                    try:
                        ex_name = serializer.data.get('experimentname')
                        #Get Report Timestep

                        opts = wn.options
                        timestepinseconds = opts.time.report_timestep
                        #print(timestepinseconds)
                        #Put New Duration
                        wn.options.time.duration = int(seconds)
                        wn.write_inpfile('basp/Water/Water.inp')
                        # Run EPANET & Convert Bin to JSON wntr
                        watersim.wntr2jsonwntr(wn,'basp/Water/jsonoutput.json')
                        #time1 = time.time() - start_time
                        # Write EPANET JSON to PostgreSQL
                        watersim.readjsonwithfiles('basp/Water/jsonoutput.json', startdate_object, timestepinseconds, final_sensors_json_file_contents, ex_name)
                        # Save Experiment Name in the database
                        newname = models.ExperimentNames(ex_name=serializer.data.get('experimentname'), ex_sensor_filename=str(filename))
                        newname.save()
                        return Response(status=status.HTTP_200_OK, data={'startdate': startdate, 'enddate': enddate, 'message': 'simulation completed', 'water interface': grafanaurl})# 'transportation interface':'http://localhost:3001/d/4YdONpXGk/transportation?orgId=1&from=1617570000000&to=1617656399000'})
                    except:
                        return Response(status=status.HTTP_400_BAD_REQUEST, data={'startdate': startdate, 'enddate': enddate, 'message': 'simulation not completed'})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'experimentname is reserved'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def testfunction():
    # try:
    #     client = InfluxDBClient(host='influxdb', port=8086, username='kios', password='kios1234!',
    #                             database='virtual_city')
    # except:
    #     client.close()
    # query = "SELECT sensor_value FROM water_output_test010_scada_sensors"
    # result = client.query(query)
    # client.close()
    # print(result)
    # wn = wntr.epanet.io.InpFile.read(wn,inp_file)

    inp_file = '/usr/src/app/basp/Water/Water.inp'
    wn = wntr.network.WaterNetworkModel (inp_file)

    #Pipe breaks or leaks
    wn = wntr.morph.split_pipe (wn, 'p123', '123_B', '123_leak_node')
    leak_node = wn.get_node ('123_leak_node')
    leak_node.add_leak (wn, area = 0.05, start_time = 2 * 3600, end_time = 12 * 3600)

    wn.write_inpfile ('filename.inp')
    # t = wntr.graphics.plot_network (wn, title = wn.name)

    # wntr.epanet.io.InpFile.write(wn,'/usr/src/app/basp/Water/Water.inp',wn,'AFD')
