import json
import re
import urllib.request


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3:4b"


def llamar_llm(prompt):
    datos = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "think": False
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(datos).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(request, timeout=120) as response:
        resultado = json.loads(response.read().decode("utf-8"))

    return resultado["response"]


def version_vulnerable(cwe1, cwe2):
    # La entrada del usuario se concatena directamente al prompt.
    prompt = f"Explain briefly the difference between {cwe1} and {cwe2}."

    print("\n--- PROMPT ENVIADO A LA LLM ---")
    print(prompt)

    print("\n--- RESPUESTA DE LA LLM ---")
    print(llamar_llm(prompt))


def cwe_valido(valor):
    # Allowlist de formato: solo CWE seguido de números.
    return re.fullmatch(r"CWE-\d+", valor) is not None


def version_mitigada(cwe1, cwe2):
    if not cwe_valido(cwe1) or not cwe_valido(cwe2):
        print("\n[!] Entrada rechazada.")
        print("Solo se permiten identificadores con formato CWE-NUMERO.")
        return

    prompt = f"Explain briefly the difference between {cwe1} and {cwe2}."

    print("\n--- PROMPT ENVIADO A LA LLM ---")
    print(prompt)

    print("\n--- RESPUESTA DE LA LLM ---")
    print(llamar_llm(prompt))


def main():
    print("=" * 50)
    print("CWE-77 - COMMAND INJECTION DEMO")
    print("=" * 50)

    print("\n1 - Version vulnerable")
    print("2 - Version mitigada")

    opcion = input("\nSeleccione una opcion: ")

    cwe1 = input("Primer CWE: ")
    cwe2 = input("Segundo CWE: ")

    if opcion == "1":
        version_vulnerable(cwe1, cwe2)

    elif opcion == "2":
        version_mitigada(cwe1, cwe2)

    else:
        print("Opcion invalida.")


if __name__ == "__main__":
    main()