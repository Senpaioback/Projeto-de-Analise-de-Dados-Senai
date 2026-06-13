import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#1. carregar o arquivo
df = pd.read_csv('Sample - Superstore.csv', encoding='windows-1252')

#2. visualizar as primeiras linhas
print("---PRIMEIRAS LINHAS DO DATASET---")
display(df.head())

#. ver o nome das colunas e os tipos de dados atuais
print("\n---ESTRUTURA DAS COLUNAS---")
df.info()

print("--- TRATAMENTO DE DADOS ---")

#1. Verificar e remover duplicados
duplicados = df.duplicated()
print(f"Linhas duplicadas encontradas: {duplicados.sum()}") # changed to sum for better output
df = df.drop_duplicates()

#2. Verificar Valores Nulos
print("\nValores nulos encontrados:")
print(df.isnull().sum())

#3. Padronizar o nome das colunas (remover espaço e colocar em minúsculo para facilitar)
df.columns = df.columns.str.replace(' ','_').str.replace('-', '_').str.lower()
print("\nNovos nomes das colunas padronizadas:")
print(df.columns.tolist()) # display the new column names

#4 converter colunas da data de texto para o tipo datetime do Pandas
if 'order_date' in df.columns: # Changed 'oder_date' and 'colums' to 'order_date' and 'columns'
    df['order_date'] = pd.to_datetime(df['order_date'])
    #Criar uma coluna de ano-mês para ajudar na análise temporal posterior
    df['ano_mes'] = df['order_date'].dt.to_period('M')

print("\nTratamento concluído com sucesso")

# Agrupando por categoria e somando as vendas e lucros
analise_categoria = df.groupby('category')[['sales', 'profit']].sum().sort_values(by='profit', ascending=False).reset_index()

# Agrupando pela taxa de desconto para ver o lucro médio
analise_desconto = df.groupby('discount')['profit'].mean().reset_index()

print("\n---Lucro medio por percentual de desconto ---")
print(analise_desconto)

#configurando o estilo do grafico
sns.set_theme(style="whitegrid")

# Gráfico 1: Lucro por Categoria
plt.figure(figsize=(8, 5))
sns.barplot(data=analise_categoria, x='category', y='profit', palette='viridis')
plt.title('lucro total por categoria de produto', fontsize=14, fontweight='bold')
plt.xlabel('categoria', fontsize=12)
plt.ylabel('Lucro acumulado ($)', fontsize=12)
plt.tight_layout()
plt.savefig('Lucro_por_categotia.png', dpi=300)
plt.show()

#Grafico 2: Desconto vs Lucro (Grafico de dispersão)
plt.figure(figsize=(9, 5))
sns.scatterplot(data=df, x='discount', y='profit', alpha=0.5, color='crimson')
plt.axhline(0, color='black', linestyle='--', linewidth=1)
plt.title('Relação entre desconto aplicado e lucro/prejuizo', fontsize=14, fontweight='bold')
plt.xlabel('desconto (proporção)', fontsize=12)
plt.ylabel('Lucro da Transação ($)', fontsize=12)
plt.tight_layout()
plt.savefig('Desconto_vs_lucro.png', dpi=300)
plt.show()