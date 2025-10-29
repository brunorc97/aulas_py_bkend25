from datetime import datetime
import locale

# Obter a data e hora atual
data_atual = datetime.now() # formato "feio"
print(data_atual)

# Formatar a data
data_formatada = data_atual.strftime("%d/%m/%Y %H:%M:%S") #formato ajustado
print("Data formatada:", data_formatada)



# Definindo a localização (exemplo: português do Brasil)
locale.setlocale(locale.LC_TIME, "pt_BR.utf8")

# Data atual
data__atual = datetime.now()

# Formatando com base na cultura
data_formatada_cultura = data__atual.strftime("%A, %d de %B de %Y")
print("Data formatada com cultura:", data_formatada_cultura)


