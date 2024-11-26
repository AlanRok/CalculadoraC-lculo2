import sympy as sy                           #Biblioteca para calcular as funções(derivar)
import matplotlib.pyplot as plt              #Biblioteca para gerar gráficos 2D (uma variável)
import numpy as np                           #Biblioteca para trabalhar com arrays e operações matemáticas
from mpl_toolkits.mplot3d import Axes3D      #Biblioteca para gerar gráficos 3D (duas variáveis)
import re                                    #Biblioteca para conversão de notações matemáticas como a² e a³ para a notação ** usada em Python.

variaveis = sy.symbols('a:z')


def derivar_funcao(expressao_str, *variaveis_derivacao):
    try:
        expressao_formatada = converter_potencias(expressao_str)
        expressao = sy.sympify(expressao_formatada)

        derivadas = {}
        for var in variaveis_derivacao:
            derivadas[var] = sy.diff(expressao, var)
        return derivadas, expressao
    except Exception as e:
        return f"Erro ao processar a função: {e}"

def converter_potencias(expressao):
    expressao = re.sub(r'(\w)²', r'\1**2', expressao)
    expressao = re.sub(r'(\w)³', r'\1**3', expressao)
    expressao = re.sub(r'(\w)\^(\d+)', r'\1**\2', expressao)
    return expressao

def calcular_dominio_imagem(funcao, variaveis):
    """
    Calcula uma estimativa simbólica do domínio da função.
    """
    try:
        singularidades = set()
        for var in variaveis:
            singularidades = singularidades.union(sy.singularities(funcao, var))

        dominio = f"Reais, exceto {singularidades}" if singularidades else "Todos os Reais"
        imagem = "Estimativa visual; calculável via intervalos numéricos."
        return dominio, imagem
    except Exception as e:
        return f"Erro ao calcular domínio/imagem: {e}", None

def gerar_grafico(expressao, variaveis):
    try:
        if len(variaveis) == 1:  #Gráfico 2D (uma variável)
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

        elif len(variaveis) == 2:  #Gráfico 3D (duas variáveis)
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

        elif len(variaveis) == 3:  #Mensagem para quando tiver 3 ou mais variáveis
            var1, var2, var3 = variaveis
            print("Gráficos 3D para funções com três variáveis não são facilmente visualizados em uma única projeção.")
        else:
            print("Não é possível gerar gráficos para funções com mais de 3 variáveis.")

    except Exception as e:
        print(f"Erro ao gerar gráfico: {e}")





funcao = input("Digite a função (exemplo: a² + b*c + c³): ")
variaveis = input("Digite as variáveis para derivar separadas por vírgula (ex: a,b,c): ")

variaveis_derivacao = [sy.symbols(var.strip()) for var in variaveis.split(",")]
resultado = derivar_funcao(funcao, *variaveis_derivacao)




if isinstance(resultado, tuple):
    derivadas, expressao = resultado
    for var, derivada in derivadas.items():
        print(f"Derivada de f em relação a {var}: {derivada}")

    #Calcular domínio e imagem
    dominio, imagem = calcular_dominio_imagem(expressao, variaveis_derivacao)
    print(f"Domínio: {dominio}")
    print(f"Imagem: {imagem}")

    #Gerar o gráfico
    gerar_grafico(expressao, variaveis_derivacao)
else:
    print(resultado)
