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

versao = 9.1                  # versão do postgrespl
your_password = new_passaword # colocar nova senha do postgres
local_pg_hba.conf = /etc/postgresql/$versao/main/pg_hba.conf

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

for pacotes in "$(cat pacotes.txt)" 
    do 

        sudo apt-get install "$pacotes" 
        echo "y"    # para confirmar as instalações

    done

#------------------------------[ pode ser feito manualmente ]-----------------------------------
# site para configuração manual: https://help.ubuntu.com/14.04/serverguide/postgresql.html

echo "listen_addresses = 'localhost'" >> ~/etc/postgresql/"$versao"/main/postgresql.conf

# alterar senha do usuario postgres
sudo -u postgres psql template1
echo "ALTER USER postgres with encrypted password "$your_password";"
echo"\q"

# sed substitui peed por md5
echo "$(sed 's/peed/md5/' "$local_pg_hba.conf")" > "$local_pg_hba.conf"

sudo service postgresql restart






