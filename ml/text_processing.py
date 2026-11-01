def preparar_texto(title: str, description: str) -> str:
    titulo_limpo = title.strip()
    descricao_limpa = description.strip()

    if titulo_limpo and descricao_limpa:
        texto = titulo_limpo + " " + descricao_limpa
    elif titulo_limpo or descricao_limpa:
        texto = titulo_limpo + descricao_limpa
    else:
        texto = ""

    return texto


if __name__ == "__main__":
    title = input("Digite o titulo: ")
    description = input("Digite a descrição: ")

    print(preparar_texto(title, description))
