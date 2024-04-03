#!/usr/bin/python3
import os, inspect, sys, shutil, json;

CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())));
ROOT = os.path.dirname(CURRENTDIR);

arquivos_negados = ['README.md', '.gitignore', '.git', '__pycache__'];
termos_negados = [];
path_projeto = ROOT;
path_deploy = "/tmp/ggh";
dados = json.loads( open(ROOT + "/data/versao.json").read() );

def copiar_recursivo(path):
    lista = os.listdir(path);
    for elemento in lista:
        if elemento in arquivos_negados:
            continue;
        buffer_path = path + "/" + elemento;
        if os.path.isdir( buffer_path ):
        	copiar_recursivo( buffer_path );
        else:
        	os.makedirs(os.path.dirname(path_deploy + buffer_path[ len(path_projeto): ]), exist_ok=True)
        	shutil.copyfile( buffer_path, path_deploy + buffer_path[ len(path_projeto): ]  );

def main():
    if os.path.exists(path_deploy):
        shutil.rmtree(path_deploy);
    os.mkdir(path_deploy);
    copiar_recursivo( path_projeto );
    path_targz = "/tmp/ggh_"+ dados["versao"] +".tar.gz";
    if os.path.exists(path_targz):
    	os.unlink(path_targz);
    os.system("cd /tmp/ && tar czf "+ path_targz +" ggh/")

main();

