import re
import json
import unicodedata
from datetime import date, timedelta


def normalizar_texto(texto):
    return unicodedata.normalize("NFD", texto).encode("ascii", "ignore").decode("utf-8")


def limpar_descricao(descricao):
    artigos = [
        "um", "uma", "o", "a", "os", "as",
        "meu", "minha", "meus", "minhas",
        "seu", "sua", "seus", "suas",
        "no", "na", "num", "numa",
        "em", "com"
    ]

    palavras = descricao.split()

    while palavras and palavras[0] in artigos:
        palavras.pop(0)

    return " ".join(palavras)


def carregar_gastos():
    try:
        with open("gastos.json", "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []


def salvar_gastos(gastos):
    with open("gastos.json", "w", encoding="utf-8") as arquivo:
        json.dump(gastos, arquivo, ensure_ascii=False, indent=4)


categorias = {
    "assinaturas": ["netflix", "spotify", "prime", "youtube", "xbox", "disney"],
    "alimentacao": ["mercado", "lanche", "restaurante", "ifood"],
    "transporte": ["uber", "gasolina", "onibus"],
    "saude": ["farmacia", "remedio", "academia"],
    "lazer": ["cinema", "passeio", "show", "viagem"],
    "investimentos": ["investi", "caixinha", "acoes", "cdb", "tesouro"],
    "animais": ["racao", "pet", "veterinario"],
    "cartao": ["cartao", "credito", "debito", "fatura"],
    "outros": [],
}


def identificar_categoria(descricao):
    descricao = normalizar_texto(descricao)
    palavras_descricao = descricao.split()

    for categoria, palavras in categorias.items():
        for palavra in palavras:
            palavra = normalizar_texto(palavra)
            if (" " in palavra and palavra in descricao) or (" " not in palavra and palavra in palavras_descricao):
                return categoria
    return "outros"


gastos = carregar_gastos()

print("Bot financeiro iniciado.")
print("Digite: um gasto, ver gastos ou sair.")

while True:
    mensagem = normalizar_texto(
        input("\nDigite uma mensagem: ").lower().strip())

    if mensagem == "sair":
        print("Encerrando bot...")
        break

    elif mensagem.startswith("ver gastos"):
        print("\n--- LISTA DE GASTOS ---")
        hoje = str(date.today())
        ontem = str(date.today() - timedelta(days=1))
        gastos_filtrados = gastos

        if "hoje" in mensagem:
            gastos_filtrados = [g for g in gastos if g["data"] == hoje]
        elif "ontem" in mensagem:
            gastos_filtrados = [g for g in gastos if g["data"] == ontem]
        else:
            for categoria in categorias.keys():
                if categoria in mensagem:
                    gastos_filtrados = [
                        g for g in gastos if g["categoria"] == categoria]
                    break

        if not gastos_filtrados:
            print("Nenhum gasto encontrado para o filtro solicitado.")
        else:
            for i, gasto in enumerate(gastos_filtrados, start=1):
                print(
                    f"{i}. {gasto['descricao']} - R${gasto['valor']:.2f} - {gasto['data']} - {gasto['categoria']}")

    else:
        verbos = r"(gastei|paguei|comprei)"
        conectores = r"(com|no|na|em|num|numa|em um|em uma|com um|com uma)"
        valor_padrao = r"(\d+(?:[.,]\d+)?)"
        data_padrao = r"(hoje|ontem)?"

        padrao1 = rf"^{data_padrao}\s*{verbos}\s+{valor_padrao}\s+{conectores}\s+(.+)$"
        padrao2 = rf"^{data_padrao}\s*{verbos}\s+(.+)\s+por\s+{valor_padrao}$"

        resultado1 = re.match(padrao1, mensagem)
        resultado2 = re.match(padrao2, mensagem)

        if resultado1:
            data_texto, _, valor, _, descricao = resultado1.groups()
        elif resultado2:
            data_texto, _, descricao, valor = resultado2.groups()
        else:
            print("Não foi possível identificar um gasto na mensagem.")
            continue

        descricao = limpar_descricao(descricao)
        valor = float(valor.replace(",", "."))
        data_gasto = date.today() - timedelta(days=1 if data_texto == "ontem" else 0)
        categoria = identificar_categoria(descricao)

        gasto = {
            "descricao": descricao,
            "valor": valor,
            "data": str(data_gasto),
            "categoria": categoria
        }

        gastos.append(gasto)
        salvar_gastos(gastos)

        print("\n--- GASTO REGISTRADO ---")
        print(f"Descrição: {descricao}")
        print(f"Valor: R${valor:.2f}")
        print(f"Data: {data_gasto}")
        print(f"Categoria: {categoria}")
