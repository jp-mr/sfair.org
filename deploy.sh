#!/bin/bash
#
# deploy.sh
#
# automatização do deploy de aplicações django/python
#
# 201618051500: João Paulo, Maio de 2016
#   
#   
#                                                      
#-----------------[ Não use servidores compartilhados (shared hosting) ]-----------------------
#   
#   
#   - NGNIX para servir conteúdo estático e rediredionar as requisições para o GUNICORN
#   - GUNICORN como servidor de aplicação
#   - SUPERVISOR para gerenciar os processos do GUNICORN
#   - POSTGRESQL como banco de dados
#   - SENTRY para gerenciar possíveis erros em produção
#   

VERSAO = ~/etc/postgresql/9.1/main/postgresql.conf # versão do postgrespl
YOUR_PASSWORD = new_passaword                      # colocar nova senha do postgres
LOCAL_PG_HBA.CONF = /etc/postgresql/$VERSAO/main/pg_hba.conf
NGINX = /etc/init.d/nginx
NEW_PROJECT = https://github.com/

#-------------------------------------[ instalação ]-----------------------------------------
#   
# Colocar no sfair.org/pacotes.txt SOMENTE os programas/pacotes necessarios para instalação 
# inicial do projeto
#
#   - vim (para não usar o vi (padrão)) 
#   - build-essential (compiladores de C/C++)
#   - python-dev (bibliotecas de compilação do python)
#   - python-psycopg2 (integração do python com o postgresql)
#   - python-virtualenv (ambientes virtuais no python)
#   - git-core (clonar o projeto)
#   - postgresql
#

for PACOTES in "$(cat pacotes.txt)" 
    do 

        sudo apt-get install "$PACOTES" 
        echo "y"    # para confirmar as instalações

    done

#------------------------------[ pode ser feito manualmente ]-----------------------------------
# site para configuração manual: https://help.ubuntu.com/14.04/serverguide/postgresql.html

echo "listen_addresses = 'localhost'" >> "$VERSAO"

# alterar senha do usuario postgres
sudo -u postgres psql template1
echo "ALTER USER postgres with encrypted password "$YOUR_PASSWORD";"
echo "\q"

# sed substitui peed por md5
echo "$(sed 's/peed/md5/' "$LOCAL_PG_HBA.CONF")" > "$LOCAL_PG_HBA.CONF"

# sudo service postgresql restart   # esta no site do ubunto
sudo /etc/init.d/postgresql restart # no video

#----------------------------------[ criação do database ]---------------------------------------

createdb -U postgres shortener # para a aplicação
echo "$YOUR_PASSAWORD"

createdb -U postgres sentry # para o sentry
echo "$YOUR_PASSAWORD"

#-------------------------------------------[ nginx ]--------------------------------------------

sudo "$NGINX" restart

#----------------------------------------[ aplicação ]-------------------------------------------

# criação do diretorio /deploy na raiz
sudo mkdir /deploy/

# permição root dentro do diretorio /deploy
# XXX acho perigoso isso!!! 
sudo chown vagrant:root /deploy/ -R

mkdir /deploy/sites # para colocar a aplicação
mkdir /deploy/venvs # para colocar o virtualenvs

#-------------------------------------[ criação ambiente virtual ]-----------------------------

virtualenv --system-site-packages shortener /deploy/venvs
virtualenv --system-site-packages sentry /deploy/venvs

source ~/deploy/venvs/shortener/bin/activate # ativação do ambiente virtual

#------------------------------------------[ projeto ]-----------------------------------------

git clone "$NEW_PROJECT" /deploy/sites/ # clonar projeto do github
