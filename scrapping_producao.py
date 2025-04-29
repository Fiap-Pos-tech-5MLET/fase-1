import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'output', 'producao')

def clean_quantity(value):
    value = value.replace('.', '').replace('-', '0')
    return int(value) if value.isdigit() else 0

def busca_recursiva(ano=None):

    # Url base
    url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02'

    # Faço a busca do proximo ano
    if ano is not None:
        url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02&ano=' + str(ano)

    
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')
        print(soup.title)
        print(soup.title.string)

        # btn_neutral = soup.find(attrs={"id": "neutral"})
        btn_prev_year = soup.find("button", id="neutral").find_previous_sibling()
        
        prev_year = btn_prev_year.attrs['value']
        ano_pesquisa = soup.find(attrs={"name": "ano", "type": "number"})

        year_min = ano_pesquisa.attrs['min']
        year_max = ano_pesquisa.attrs['max']

        table = soup.find('table', {'class': 'tb_base tb_dados'})

        #xtrai as linhas da tabela
        rows = table.find_all('tr')

        # Lista para armazenar os dados
        data = []

        last_group = ''
        # Itera sobre as linhas da tabela
        for row in table.find_all('tr'):
            cells = row.find_all(['th', 'td'])
            
            if len(cells) == 2:  # Apenas linhas com duas células
                product_cell, quantity_cell = cells
                
                # Identifica o tipo de item
                if 'tb_item' in product_cell.get('class', []):
                    current_category = product_cell.get_text(strip=True)
                    data.append({
                        'Categoria Principal': current_category,
                        'Subcategoria': '-',
                        'Quantidade (L)': quantity_cell.get_text(strip=True)
                    })
                elif 'tb_subitem' in product_cell.get('class', []):
                    data.append({
                        'Categoria Principal': current_category,
                        'Subcategoria': product_cell.get_text(strip=True),
                        'Quantidade (L)': quantity_cell.get_text(strip=True)
                    })
                # elif 'tb_total' in row.find_parent('tfoot').get('class', []):
                else:
                    # Opcional: tratamento para o total
                    pass

        #converte os dados em um dataframe do pandas
        # df = pd.DataFrame(data[1:], columns=data[0]) # A linha 0 é o cabeçalho
        df = pd.DataFrame(data)
        # Função para limpar valores numéricos
        
        # Aplica a limpeza
        df['Quantidade (L)'] = df['Quantidade (L)'].apply(clean_quantity)

        # Exibe as primeiras linhas
        # print(df.head(100))

        filename = f"vitibrasil_{int(prev_year) + 1}.html" if prev_year else "vitibrasil.html"

        # grava os dados em csv
        df.to_csv(os.path.join(DATA_DIR, filename.replace('.html', '.csv')), index=False, encoding='utf-8', sep=';', doublequote=True)

        # salva o html na pasta para consultas
        with open( os.path.join(DATA_DIR, filename), 'w', encoding='utf-8') as file:
            file.write(html_content)
            print(f"Arquivo {filename} salvo com sucesso!")

        # print("Pagina obtida")

        if prev_year < year_min:
            print("Ano minimo atingido!")
            print("Processamento concluido")
            return
        
        busca_recursiva(prev_year)

    else:
        print("Erro ao obter a pagina")
        exit()


busca_recursiva()