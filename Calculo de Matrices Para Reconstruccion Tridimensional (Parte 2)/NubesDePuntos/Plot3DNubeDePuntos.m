clc
clear all
close all

%Solucion Positiva
file = 'ArchivoDeNubeDePuntosPositiva_2014-12-05 17:47:41.256356.txt'
puntos3D = importdata(file);

scatter3(puntos3D(:,1),puntos3D(:,2),puntos3D(:,3));
hold on


%Solucion Negativa
%file = 'ArchivoDeNubeDePuntosNegativa_2014-12-01 16:27:14.271763.txt'
%puntos3D = importdata(file);

%scatter3(puntos3D(:,1),puntos3D(:,2),puntos3D(:,3));
%hold on

axis on;
axis equal;