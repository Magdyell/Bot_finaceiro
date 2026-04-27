import re
import json
import unicodedata
from datetime import date, timedelta
import firebase_admin
from firebase_admin import credentials, firestore
import time


if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()


def normalizar_texto(texto):
    return unicodedata.normalize("NFD", texto).encode("ascii", "ignore").decode("utf-8")


comandos_listar = [
    "ver gastos", "listar gastos", "mostrar gastos", "exibir gastos",
    "gastos hoje", "gastos ontem", "gastos assinaturas",
    "gastos alimentacao", "gastos transporte", "gastos saude",
    "gastos lazer", "gastos investimentos", "gastos animais",
    "gastos cartao", "quanto gastei hoje", "quanto gastei ontem",
]


categorias = {
    "assinaturas": ["netflix", "spotify", "prime", "youtube", "xbox", "disney"],
    "alimentacao": ["mercado", "lanche", "restaurante", "ifood", "comida", "supermercado", "pizza", "hamburguer", "bolo", "padaria", "cafe", "bar", "bebida"],
    "transporte": ["uber", "gasolina", "onibus", "combustivel"],
    "saude": ["farmacia", "remedio", "academia"],
    "lazer": ["cinema", "passeio", "show", "viagem"],
    "investimentos": ["investi", "caixinha", "acoes", "cdb", "tesouro"],
    "animais": ["racao", "pet", "veterinario"],
    "cartao": ["cartao", "credito", "debito", "fatura"],
    "outros": [],
}

def vincular_whatsapp(mensagem, numero_usuario):
    partes = mensagem.split()

    if len(partes) < 2:
        return "Envie assim: vincular 123456"

    codigo = partes[1].strip()
    numero = normalizar_numero(numero_usuario)

    usuarios_ref = db.collection("usuarios")
    consulta = usuarios_ref.where("codigoVinculacaoWhatsapp", "==", codigo).limit(1).stream()

    for usuario in consulta:
        doc_ref = db.collection("usuarios").document(usuario.id)

        doc_ref.update({
            "whatsapp": numero,
            "codigoVinculacaoWhatsapp": firestore.DELETE_FIELD
        })

        return "✅ WhatsApp vinculado com sucesso à sua conta!"

    return "Código inválido ou expirado."


def normalizar_numero(numero):
    numero = re.sub(r"\D", "", str(numero))

    if numero.startswith("55"):
        return numero

    return f"55{numero}"


def obter_uid_usuario(numero_usuario):
    numero = normalizar_numero(numero_usuario)

    usuarios_ref = db.collection("usuarios")
    consulta = usuarios_ref.where("whatsapp", "==", numero).limit(1).stream()

    for usuario in consulta:
        return usuario.id

    return None


def carregar_gastos_firebase(numero_usuario):
    uid = obter_uid_usuario(numero_usuario)

    if not uid:
        return []

    doc_ref = db.collection("usuarios").document(uid)
    doc = doc_ref.get()

    if not doc.exists:
        return []

    dados = doc.to_dict()
    return dados.get("gastos", []) if isinstance(dados.get("gastos", []), list) else []


def salvar_gastos_firebase(numero_usuario, gastos_usuario):
    uid = obter_uid_usuario(numero_usuario)

    if not uid:
        return False

    doc_ref = db.collection("usuarios").document(uid)

    doc_ref.set({
        "gastos": gastos_usuario
    }, merge=True)

    return True


def extrair_valor(mensagem):
    padrao_valor = r"(?:r\$?\s*)?(\d+(?:[.,]\d+)?)(?:\s*(?:real|reais|rs|r))?"
    resultado = re.search(padrao_valor, mensagem)

    if resultado:
        return float(resultado.group(1).replace(",", "."))

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
    texto = re.sub(r"(?:r\$?\s*)?\d+(?:[.,]\d+)?(?:\s*(real|reais|rs|r))?", "", texto)

    texto = texto.strip()
    return limpar_descricao(texto)


def identificar_categoria(descricao):
    descricao = normalizar_texto(descricao)
    palavras_descricao = descricao.split()

    for categoria, palavras in categorias.items():
        for palavra in palavras:
            palavra = normalizar_texto(palavra)

            if (" " in palavra and palavra in descricao) or (
                " " not in palavra and palavra in palavras_descricao
            ):
                return categoria

    return "outros"


def gerar_total_por_categoria(gastos_usuario):
    if not gastos_usuario:
        return "Nenhum gasto registrado ainda."

    totais = {}

    for gasto in gastos_usuario:
        categoria = gasto["categoria"]
        valor = gasto["valor"]
        totais[categoria] = totais.get(categoria, 0) + valor

    resposta = "📊 Total por categoria:\n\n"

    for categoria, total in totais.items():
        resposta += f"• {categoria}: R${total:.2f}\n"

    return resposta


def gerar_total(gastos_usuario, mensagem):
    hoje = str(date.today())
    ontem = str(date.today() - timedelta(days=1))

    gastos_filtrados = gastos_usuario

    if "hoje" in mensagem:
        gastos_filtrados = [g for g in gastos_usuario if g["data"] == hoje]

    elif "ontem" in mensagem:
        gastos_filtrados = [g for g in gastos_usuario if g["data"] == ontem]

    categoria_filtrada = ""

    for categoria in categorias.keys():
        if categoria in mensagem:
            gastos_filtrados = [
                g for g in gastos_filtrados if g["categoria"] == categoria
            ]
            categoria_filtrada = categoria
            break

    if not gastos_filtrados:
        return "Nenhum gasto encontrado para esse filtro."

    total = sum(g["valor"] for g in gastos_filtrados)

    texto_data = ""
    if "hoje" in mensagem:
        texto_data = " hoje"
    elif "ontem" in mensagem:
        texto_data = " ontem"

    texto_categoria = f" em {categoria_filtrada}" if categoria_filtrada else ""

    return f"💰 Você gastou R${total:.2f}{texto_categoria}{texto_data}."


def listar_gastos(gastos_usuario, mensagem):
    hoje = str(date.today())
    ontem = str(date.today() - timedelta(days=1))

    gastos_filtrados = gastos_usuario

    if "hoje" in mensagem:
        gastos_filtrados = [g for g in gastos_usuario if g["data"] == hoje]

    elif "ontem" in mensagem:
        gastos_filtrados = [g for g in gastos_usuario if g["data"] == ontem]

    else:
        for categoria in categorias.keys():
            if categoria in mensagem:
                gastos_filtrados = [
                    g for g in gastos_usuario if g["categoria"] == categoria
                ]
                break

    if not gastos_filtrados:
        return "Nenhum gasto encontrado para esse filtro."

    resposta = "📋 Lista de gastos:\n\n"

    for i, gasto in enumerate(gastos_filtrados, start=1):
        resposta += (
            f"{i}. {gasto['descricao']} - "
            f"R${gasto['valor']:.2f} - "
            f"{gasto['data']} - "
            f"{gasto['categoria']}\n"
        )

    return resposta


def registrar_gasto(mensagem, numero_usuario, gastos_usuario):
    valor = extrair_valor(mensagem)

    if valor is None:
        return "Não consegui identificar o valor. Exemplo: gastei 50 mercado"

    data_gasto = extrair_data(mensagem)
    descricao = extrair_descricao(mensagem)

    if not descricao:
        return "Não consegui identificar a descrição. Exemplo: gastei 50 mercado"

    categoria = identificar_categoria(descricao)

    gasto = {
        "id": int(time.time() * 1000),
        "descricao": descricao,
        "valor": valor,
        "data": str(data_gasto),
        "categoria": categoria,
        "status": "pendente"
    }

    gastos_usuario.append(gasto)
    salvou = salvar_gastos_firebase(numero_usuario, gastos_usuario)

    if not salvou:
        return "Seu número ainda não está vinculado a uma conta do sistema."

    return (
        "✅ Gasto registrado!\n\n"
        f"Descrição: {descricao}\n"
        f"Valor: R${valor:.2f}\n"
        f"Data: {data_gasto}\n"
        f"Categoria: {categoria}\n"
        f"Status: pendente"
    )


def processar_mensagem(mensagem, numero_usuario):
    mensagem = normalizar_texto(mensagem.lower().strip())
    def processar_mensagem(mensagem, numero_usuario):
     print("NUMERO ORIGINAL:", numero_usuario)
     print("NUMERO NORMALIZADO:", normalizar_numero(numero_usuario))

    mensagem = normalizar_texto(mensagem.lower().strip())
    if mensagem.startswith("vincular"):
        return vincular_whatsapp(mensagem, numero_usuario)

    if mensagem in ["oi", "ola", "olá", "menu", "ajuda"]:
        return (
            "🤖 Bot Financeiro\n\n"
            "Você pode me enviar:\n"
            "• gastei __ no mercado\n"
            "• paguei __ com uber ontem\n"
            "• ver gastos\n"
            "• gastos hoje\n"
            "• quanto gastei hoje\n"
            "• total por categoria"
        )

    uid = obter_uid_usuario(numero_usuario)

    if not uid:
        return "Seu número ainda não está cadastrado no sistema."

    gastos_usuario = carregar_gastos_firebase(numero_usuario)

    if mensagem == "total por categoria":
        return gerar_total_por_categoria(gastos_usuario)

    if "quanto gastei" in mensagem:
        return gerar_total(gastos_usuario, mensagem)

    if any(mensagem.startswith(cmd) for cmd in comandos_listar):
        return listar_gastos(gastos_usuario, mensagem)

    return registrar_gasto(mensagem, numero_usuario, gastos_usuario)
