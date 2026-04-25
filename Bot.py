import re
import json
import unicodedata
from datetime import date, timedelta


def normalizar_texto(texto):
    return unicodedata.normalize("NFD", texto).encode("ascii", "ignore").decode("utf-8")

comandos_listar = [
    "ver gastos", "listar gastos",
    "mostrar gastos", "exibir gastos",
    "gastos hoje", "gastos ontem",
    "gastos assinaturas", "gastos alimentacao",
    "gastos transporte", "gastos saude",
    "gastos lazer", "gastos investimentos",
    "gastos animais", "gastos cartao",
    "quanto gastei hoje", "quanto gastei ontem",
]

def extrair_valor(mensagem):
    padrao_valor = r"(?:r\$?\s*)?(\d+(?:[.,]\d+)?)(?:\s*(?:real|reais|rs|r))?"
    resultado = re.search(padrao_valor, mensagem)

    if resultado:
        valor = resultado.group(1).replace(",", ".")
        return float(valor)

    return None


def extrair_data(mensagem):
    hoje = date.today()

    if "ontem" in mensagem:
        return hoje - timedelta(days=1)

    return hoje


def limpar_descricao(descricao):
    artigos = [
        "um", "uma", "o", "a", "os", "as",
        "meu", "minha", "meus", "minhas",
        "seu", "sua", "seus", "suas",
        "no", "na", "num", "numa",
        "em", "com", "por"
    ]

    palavras = descricao.split()

    while palavras and palavras[0] in artigos:
        palavras.pop(0)

    return " ".join(palavras)


def extrair_descricao(mensagem):
    texto = mensagem

    texto = re.sub(r"\b(hoje|ontem)\b", "", texto)
    texto = re.sub(r"\b(gastei|paguei|comprei)\b", "", texto)
    texto = re.sub(r"\b(por|com|no|na|em|num|numa)\b", "", texto)
    texto = re.sub(
        r"(?:r\$?\s*)?\d+(?:[.,]\d+)?(?:\s*(real|reais|rs|r))?", "", texto)

    texto = texto.strip()
    texto = limpar_descricao(texto)

    return texto


def carregar_gastos():
    try:
        with open("gastos.json", "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()

            if not conteudo:
                return []

            return json.loads(conteudo)

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        return []


def salvar_gastos(gastos):
    with open("gastos.json", "w", encoding="utf-8") as arquivo:
        json.dump(gastos, arquivo, ensure_ascii=False, indent=4)


categorias = {
    "assinaturas": ["netflix", "spotify", "prime", "youtube", "xbox", "disney"],
    "alimentacao": ["mercado", "lanche", "restaurante", "ifood"],
    "transporte": ["uber", "gasolina", "onibus", "combustivel"],
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

def mostrar_total_por_categoria(gastos):
    if not gastos:
        print("Nenhum gasto registrado.")
        return

    totais = {}

    for gasto in gastos:
        categoria = gasto["categoria"]
        valor = gasto["valor"]

        if categoria not in totais:
            totais[categoria] = 0

        totais[categoria] += valor

    print("\n--- TOTAL POR CATEGORIA ---")

    for categoria, total in totais.items():
        print(f"{categoria}: R${total:.2f}")

def calcular_total(gastos, mensagem):
    hoje = str(date.today())
    ontem = str(date.today() - timedelta(days=1))

    gastos_filtrados = gastos

    if "hoje" in mensagem:
        gastos_filtrados = [g for g in gastos_filtrados if g["data"] == hoje]

    elif "ontem" in mensagem:
        gastos_filtrados = [g for g in gastos_filtrados if g["data"] == ontem]

    for categoria in categorias.keys():
        if categoria in mensagem:
            gastos_filtrados = [g for g in gastos_filtrados if g["categoria"] == categoria]
            break

    if not gastos_filtrados:
        print("Nenhum gasto encontrado para esse filtro.")
        return

    total = sum(g["valor"] for g in gastos_filtrados)

    texto_data = ""
    if "hoje" in mensagem:
        texto_data = " hoje"
    elif "ontem" in mensagem:
        texto_data = " ontem"

    texto_categoria = ""
    for categoria in categorias.keys():
        if categoria in mensagem:
            texto_categoria = f" em {categoria}"
            break

    print(f"\nVocê gastou R${total:.2f}{texto_categoria}{texto_data}")

while True:
    mensagem = normalizar_texto(
        input("\nDigite uma mensagem: ").lower().strip())

    if mensagem == "sair":
        print("Encerrando bot...")
        break
    elif mensagem == "total por categoria":
        mostrar_total_por_categoria(gastos)
    elif "quanto gastei" in mensagem:
        calcular_total(gastos, mensagem)

    elif any(mensagem.startswith(cmd) for cmd in comandos_listar):
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
                        g for g in gastos if g["categoria"] == categoria
                    ]
                    break

        if not gastos_filtrados:
            print("Nenhum gasto encontrado para o filtro solicitado.")
        else:
            for i, gasto in enumerate(gastos_filtrados, start=1):
                print(
                    f"{i}. {gasto['descricao']} - "
                    f"R${gasto['valor']:.2f} - "
                    f"{gasto['data']} - "
                    f"{gasto['categoria']}"
                )
    else:
        valor = extrair_valor(mensagem)

        if valor is None:
            print("Não foi possível identificar o valor do gasto.")
            continue

        data_gasto = extrair_data(mensagem)
        descricao = extrair_descricao(mensagem)

        if not descricao:
            print("Não foi possível identificar a descrição do gasto.")
            continue

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
