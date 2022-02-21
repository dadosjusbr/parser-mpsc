# coding: utf8
import sys
import os

from coleta import coleta_pb2 as Coleta

from headers_keys import (CONTRACHEQUE,
                          INDENIZACOES,
                          INDENIZACOES_2021, HEADERS)
import number


def parse_employees(fn, chave_coleta, categoria):
    employees = {}
    counter = 1
    for row in fn:
        name = row[0]
        function = row[1]
        location = row[2]
        if not number.is_nan(name) and name != "Nome":
            membro = Coleta.ContraCheque()
            membro.id_contra_cheque = chave_coleta + "/" + str(counter)
            membro.chave_coleta = chave_coleta
            membro.nome = name
            membro.funcao = function.replace("\n", " ")
            membro.local_trabalho = "-" if number.is_nan(location) else location.replace("\n", " ")
            membro.tipo = Coleta.ContraCheque.Tipo.Value("MEMBRO")
            membro.ativo = True
            
            membro.remuneracoes.CopyFrom(
                cria_remuneracao(row, categoria)
            )
            
            employees[name] = membro
            counter += 1
            
    return employees


def cria_remuneracao(row, categoria):
    remu_array = Coleta.Remuneracoes()
    items = list(HEADERS[categoria].items())
    for i in range(len(items)):
        key, value = items[i][0], items[i][1]
        remuneracao = Coleta.Remuneracao()
        remuneracao.natureza = Coleta.Remuneracao.Natureza.Value("R")
        remuneracao.categoria = categoria
        remuneracao.item = key
        # Caso o valor seja negativo, ele vai transformar em positivo:
        remuneracao.valor = float(abs(number.format_value(row[value])))

        if categoria == CONTRACHEQUE and value in [12, 13, 14]:
            remuneracao.valor = remuneracao.valor * (-1)
            remuneracao.natureza = Coleta.Remuneracao.Natureza.Value("D")
        else: 
            remuneracao.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")

        if (
            categoria == CONTRACHEQUE
           ) and value in [4]:
            remuneracao.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("B")

        remu_array.remuneracao.append(remuneracao)

    return remu_array


def update_employees(fn, employees, categoria):
    for row in fn:
        name = row[1]
        if name in employees.keys():
            emp = employees[name]
            remu = cria_remuneracao(row, categoria)
            emp.remuneracoes.MergeFrom(remu)
            employees[name] = emp
    return employees


def parse(data, chave_coleta, month, year):
    employees = {}
    folha = Coleta.FolhaDePagamento()

    employees.update(parse_employees(data.contracheque, chave_coleta, CONTRACHEQUE))
    # Puts all parsed employees in the big map
    if int(year) == 2021:
        update_employees(data.indenizatorias, employees, INDENIZACOES_2021)
    else:
        update_employees(data.indenizatorias, employees, INDENIZACOES)

    for i in employees.values():
        folha.contra_cheque.append(i)
    return folha
