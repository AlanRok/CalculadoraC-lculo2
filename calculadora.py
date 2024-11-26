import sympy as sy                           # Biblioteca para calcular as funções (derivar)
import matplotlib.pyplot as plt              # Biblioteca para gerar gráficos 2D (uma variável)
import numpy as np                           # Biblioteca para trabalhar com arrays e operações matemáticas
from mpl_toolkits.mplot3d import Axes3D      # Biblioteca para gerar gráficos 3D (duas variáveis)
import re                                    # Biblioteca para conversão de notações matemáticas como a² e a³ para a notação ** usada em Python.

variaveis = sy.symbols('a:z')

def derivar_funcao(expressao_str, *variaveis_derivacao, ordem=1):
    try:
        expressao_formatada = converter_potencias(expressao_str)
        expressao = sy.sympify(expressao_formatada)

        derivadas = {}
        for var in variaveis_derivacao:
            derivadas[var] = sy.diff(expressao, var, ordem)
        return derivadas, expressao
    except Exception as e:
        return f"Erro ao processar a função: {e}"

def converter_potencias(expressao):
    expressao = re.sub(r'(\w)²', r'\1**2', expressao)
    expressao = re.sub(r'(\w)³', r'\1**3', expressao)
    expressao = re.sub(r'(\w)\^(\d+)', r'\1**\2', expressao)
    return expressao

def calcular_dominio_imagem(expressao, variaveis):
    """
    Calcula o domínio e a imagem da função em um intervalo numérico definido.
    """
    try:
        # Definir intervalos para cálculo numérico
        intervalo = np.linspace(-10, 10, 500)
        valores = []

        if len(variaveis) == 1:
            # Para funções de uma variável
            var = variaveis[0]
            f_lambdified = sy.lambdify(var, expressao, modules=['numpy'])
            valores = f_lambdified(intervalo)

        elif len(variaveis) == 2:
            # Para funções de duas variáveis
            var1, var2 = variaveis
            f_lambdified = sy.lambdify((var1, var2), expressao, modules=['numpy'])
            x, y = np.meshgrid(intervalo, intervalo)
            valores = f_lambdified(x, y)

        elif len(variaveis) == 3:
            # Para funções de três variáveis, fixar uma variável
            print("Função possui três variáveis. Será necessário fixar um valor para uma delas.")
            var1, var2, var3 = variaveis
            var_fixada = input(f"Escolha uma variável para fixar ({var1}, {var2}, {var3}): ").strip()
            
            if var_fixada not in [str(var1), str(var2), str(var3)]:
                return "Erro: Variável fixada inválida.", None
            
            valor_fixado = float(input(f"Digite o valor para {var_fixada}: "))
            vars_restantes = [v for v in variaveis if str(v) != var_fixada]
            f_lambdified = sy.lambdify((*vars_restantes, sy.symbols(var_fixada)), expressao, modules=['numpy'])
            x, y = np.meshgrid(intervalo, intervalo)
            valores = f_lambdified(x, y, valor_fixado)

        else:
            return "Erro: Domínio/imagem não suportados para mais de 3 variáveis.", None

        # Determinar o intervalo do domínio e imagem
        dominio = f"{variaveis} ∈ ({intervalo.min()}, {intervalo.max()})"
        imagem = f"f({', '.join(map(str, variaveis))}) ∈ ({np.nanmin(valores)}, {np.nanmax(valores)})"
        return dominio, imagem

    except Exception as e:
        return f"Erro ao calcular domínio/imagem: {e}", None

def gerar_grafico(expressao, variaveis):
    try:
        if len(variaveis) == 1:  # Gráfico 2D (uma variável)
            var = variaveis[0]
            f_lambdified = sy.lambdify(var, expressao, modules=['numpy'])
            
            x = np.linspace(-10, 10, 500)
            y = f_lambdified(x)

            plt.figure(figsize=(8, 6))
            plt.plot(x, y, label=str(expressao))
            plt.title("Gráfico 2D")
            plt.xlabel(str(var))
            plt.ylabel("f(x)")
            plt.legend()
            plt.grid()
            plt.show()

        elif len(variaveis) == 2:  # Gráfico 3D (duas variáveis)
            var1, var2 = variaveis
            f_lambdified = sy.lambdify((var1, var2), expressao, modules=['numpy'])

            x = np.linspace(-10, 10, 100)
            y = np.linspace(-10, 10, 100)
            x, y = np.meshgrid(x, y)
            z = f_lambdified(x, y)

            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(x, y, z, cmap='viridis')
            ax.set_title("Gráfico 3D")
            ax.set_xlabel(str(var1))
            ax.set_ylabel(str(var2))
            ax.set_zlabel("f(x, y)")
            plt.show()

        elif len(variaveis) == 3:  # Gráfico para três variáveis
            print("Função possui três variáveis. Será necessário fixar um valor para uma delas.")
            
            # Permitir ao usuário escolher a variável a ser fixada
            var1, var2, var3 = variaveis
            var_fixada = input(f"Escolha uma variável para fixar ({var1}, {var2}, {var3}): ").strip()
            
            if var_fixada not in [str(var1), str(var2), str(var3)]:
                print("Variável inválida! Certifique-se de escolher uma das variáveis disponíveis.")
                return
            
            valor_fixado = float(input(f"Digite o valor para {var_fixada}: "))

            # Determinar as variáveis restantes
            vars_restantes = [v for v in variaveis if str(v) != var_fixada]
            var1, var2 = vars_restantes
            
            f_lambdified = sy.lambdify((var1, var2, sy.symbols(var_fixada)), expressao, modules=['numpy'])

            x = np.linspace(-10, 10, 100)
            y = np.linspace(-10, 10, 100)
            x, y = np.meshgrid(x, y)
            z = f_lambdified(x, y, valor_fixado)

            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(x, y, z, cmap='viridis')
            ax.set_title(f"Gráfico 3D para {var_fixada} = {valor_fixado}")
            ax.set_xlabel(str(var1))
            ax.set_ylabel(str(var2))
            ax.set_zlabel(f"f({str(var1)}, {str(var2)}, {valor_fixado})")
            plt.show()
        else:
            print("Não é possível gerar gráficos para funções com mais de 3 variáveis.")

    except Exception as e:
        print(f"Erro ao gerar gráfico: {e}")





# Fluxo principal do programa
funcao = input("Digite a função (exemplo: a² + b*c + c³): ")
variaveis = input("Digite as variáveis para derivar separadas por vírgula (ex: a,b,c): ")
ordem_derivada = int(input("Digite a ordem da derivada (ex: 1, 2, 3): "))

variaveis_derivacao = [sy.symbols(var.strip()) for var in variaveis.split(",")]
resultado = derivar_funcao(funcao, *variaveis_derivacao, ordem=ordem_derivada)

if isinstance(resultado, tuple):
    derivadas, expressao = resultado
    for var, derivada in derivadas.items():
        print(f"Derivada de ordem {ordem_derivada} de f em relação a {var}: {derivada}")

    # Calcular domínio e imagem
    dominio, imagem = calcular_dominio_imagem(expressao, variaveis_derivacao)
    print(f"Domínio: {dominio}")
    print(f"Imagem: {imagem}")

    # Gerar o gráfico
    gerar_grafico(expressao, variaveis_derivacao)
else:
    print(resultado)
