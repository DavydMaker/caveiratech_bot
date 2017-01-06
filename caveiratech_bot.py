#!/usr/bin/python3
# -*- coding: utf-8 -*-
import telebot
import urllib.request as url
import urllib
import json
import platform
import os
from datetime import datetime

bot = telebot.TeleBot('')
logo = '''
	 ____________________________________
	|   ____  _____  _             _     |
	|  / ___||_   _|| |__    ___  | |_   |
	| | |      | |  | '_ \  / _ \ | __|  |
	| | |___   | |  | |_) || (_) || |_   |	
	|  \____|  |_|  |_.__/  \___/  \__|  |
	|____________________________________|'''

barra = '------------------------------------------------------'

#Verificar sistema operacional e limpar tela de acordo
os.system('cls' if os.name == 'nt' else 'clear')
nomeArquivo = 'CT_LOG-{data}.txt'.format(data=str(datetime.today())[:19])
nomeArquivo = nomeArquivo.replace(":",".")
arquivo = open(nomeArquivo, 'a')
arquivo.write(logo+'\n')
arquivo.write(barra+'\n')

#Gerar LOG
def log_msg(mensagem):
    return('''
[Data do Recebimento]: {data}
[Texto]: {comando}
[Tipo de Chat]: {origem}
[Titulo do Chat]: {nomechat}
[ID do Chat]: {chatid}
[Nome do Usuário]: {nome_usuario}
[Username do Usuário]: @{username}
[ID do Usuário]: {id_user}
-------------------------------------------'''.format(data=str(datetime.today()), comando=mensagem.text, origem=mensagem.chat.type, nomechat=mensagem.chat.title, chatid=mensagem.chat.id,
                               nome_usuario=mensagem.from_user.first_name, username=mensagem.from_user.username, id_user=mensagem.from_user.id))

# Verificar se usuário é admin
def verificarAdmin(id_):
	id_admins = [admin.user.id for admin in bot.get_chat_administrators(id_.chat.id)]
	if id_.from_user.id not in id_admins: return False
	else: return True

# Mostrar como contribuir
@bot.message_handler(commands=['contribuir'])
def contribuir(m):
	gerarlog(m)
	bot.reply_to(m,'''
Contribuidores:
Diego Bernardes(@EXPL01T3R0)
ReiGelado(@ReiGel_ado)

		Para contribuir com o BOT acesse:
https://github.com/DavydMaker/caveiratech_bot''')

# Mostrar comandos
@bot.message_handler(commands=['help'])
def help(m):
		gerarlog(m)
#	if verificarAdmin(m.from_user.id) == True:		
		bot.reply_to(m,'''
Lista de Comandos:

/help - Listar comandos e suas descrições
/regras - Listar regras
/admins - Listar administradores
/desenvolvedores - Listar desenvolvedores do BOT
/geoip <host> - Obter informações de geolocalização do IP informado
/contribuir - Listar contribuidores do BOT e como contribuir''')
#	else:
#		bot.send_message(m.chat.id,'''
#Lista de Comandos:

#/help - Listar comandos e suas descrições
#/regras - Listar regras
#/admins - Listar administradores
#/desenvolvedores - Listar desenvolvedores do BOT''')

# Mostrar lista de administradores do grupo
@bot.message_handler(commands=['admins'])
def admins(m):
	if m.chat.type != 'private':
		gerarlog(m)
		admins_username = [admin.user.username for admin in bot.get_chat_administrators(m.chat.id)]
		bot.reply_to(m, '''
Lista de Administradores:

@{0}
@{1}
@{2}
@{3}
'''.format(*admins_username))
	else:
		bot.reply_to(m, 'Comando desativado para chat privado.')

# Mostrar lista de desenvolvedores do BOT
@bot.message_handler(commands=['desenvolvedores'])
def desenvolvedores(m):
	gerarlog(m)
	bot.reply_to(m, '''
Lista de Desenvolvedores:

@DavydMaker
@AlobusCT''')

# Retornar dados do IP
def geoip(ip):
	conexao = url.urlopen('http://freegeoip.net/json/'+ip)
	data = conexao.read()
	json_data = json.loads(data)
	print(json_data)
	ipJ = json_data['ip']
	nomePais = json_data['country_name']
	nomeEstado = json_data['region_name']
	cidade = json_data['city']
	cep = json_data['zip_code']
	fusoHorario = json_data['time_zone']
	latitude = json_data['latitude']
	longitude = json_data['longitude']
	return('''
IP : '''+ipJ+'''
País: '''+nomePais+'''
Estado: '''+nomeEstado+'''
Cidade: '''+cidade+'''
CEP: '''+cep+'''
Fuso Horário: '''+fusoHorario+'''
Lat./Long.: '''+str(latitude)+', '+str(longitude))

# Mostrar GeoIP
@bot.message_handler(commands=['geoip'])
def geoipH(m):
#	if m.chat.type != "private":
#		if verificarAdmin(m) == True:
			gerarlog(m)
			comando = m.text.split(' ')
			try:
				bot.reply_to(m, geoip(comando[1]))
			except IndexError:
				bot.reply_to(m,'HOST não informado.\n Exemplo: /geoip caveiratech.com')
			except urllib.error.HTTPError:
				bot.reply_to(m,'Nenhum dado da HOST foi encontrado.')
			except Exception as e:
				bot.reply_to(m,'BUGOU ;-;.')
#		else:
#			bot.reply_to(m,'Permissão insuficiente para executar comando.')
#	else:
#		bot.reply_to(m,'Função apenas para grupos.') #Para que não fiquem zoando o bot em pvd, dps modifico

# Mostrar regras
@bot.message_handler(commands=['regras'])
def regras(m):
	gerarlog(m)
	bot.reply_to(m,'''
1. Política anti-harassment:
Os canais signatários deste guia são locais livres de assédio, opressão e preconceitos.
Não serão tolerados comentários ofensivos sobre gênero, orientação sexual, deficiências, aparência física, raça ou credo;Os membros do grupo não estão no grupo para paquerar, não insista, existem outras redes para isto;O uso de conteúdo adulto em forma de vídeos, gif's, imagens ou áudio não será tolerado;Termos inadequados, intimidação, perseguição, comportamento rude, ofensivo ou desrespeitoso não serão tolerados;Piadas sexistas, machistas, misóginas ou discriminatórias, contra miniorias, pessoas ou grupos não serão toleradas;Bullying não será tolerado.
Aqueles que não respeitarem tais condutas serão advertidos (em privado) e caso o comportamento persista, serão removidos do grupo ou canal.

2. Política anti-spam:
Não faça SPAM. Avalie os pontos 4.3, 4.4, 4.5 e 4.6 para referências do que é considerado propaganda não solicitada.

3. Política anti-pirataria:
Pirataria é crime, não repasse links para material protegido no grupo;Quem repassar material protegido poderá ser denunciado para o autor do material.

4. Orientações diversas:
Lembre-se que o telegram é uma rede mundial, dar bom dia, boa tarde e boa noite não faz sentido já que existem usuários em diversos fusos nos grupos, tente entender o contexto das conversas e interagir. Se preferir inicie um novo assunto com uma pergunta direta e clara, ou então compartilhe sua opinião, mas lembre-se que telegram não é real-time-chat, mande a mensagem e aguarde os usuários do grupo interagirem a seu tempo.
Não precisa pedir permissão para perguntar, muito menos perguntar se alguém conhece determinado assunto no grupo antes de informar sua dúvida. Apenas faça sua pergunta e aguarde uma interação.
Quando for responder alguma pergunta, clique nela e escolha a opção responder, pois somente assim os membros do grupo saberão que sua resposta está associada aquela determinada questão.
Lembre-se que os grupos não são canais de suporte oficiais das tecnologias relacionadas, os grupos são formados por pessoas que assim como você estão ali pra trocar experiências. Não há qualquer acordo de tempo de resposta para as dúvidas no grupo, ou seja, caso ninguém responda, é possível que elas não saibam a resposta ou talvez não tiveram tempo disponível para responder.
Tente descrever sua dúvida com o máximo de detalhes possíveis, perguntas vagas e superficiais tem menor chance de obter resposta.

4.1 Tema dos grupos:
Sempre que possível mantenha o tema central do grupo nas conversas;Evite temas off-topics como games, futebol, credo e política;Chame seu colega para um grupo off-topic ou em PVT para discutir esses temas se desejar.

4.2 Divulgar vagas de emprego:
Não divulgue vagas de emprego sem consultar os admins (em pvt);Não divulgue vagas de emprego que não estejam ligadas ao tema do grupo ou relacionadas com TI;Se preferir, existem canais no telegram específicos para este tipo de atividade.

4.3 Divulgar canais:
Não divulgue outros grupos ou canais sem consultar os admins (em pvt);Se for autorizado pelos admins, ainda assim, evite fazer flood com o link do grupo.

4.4 Divulgar eventos:
Não divulgue eventos sem consultar os admins (em pvt);Se for autorizado pelos admins, ainda assim, evite fazer flood com infos do evento no grupo.

4.5 Compartilhar links:
Evite fazer flood de links no canal;Se quiser passar muitos links ou muito material, o ideal é fazer um blogpost e compartilhar o link no grupo;Em hipótese alguma serão tolerados links com anúncios para visualização (como adf.ly e similares). Para compartilhar links, poste a URL direta do material proposto.

4.6 Divulgar produtos e serviços:
Não divulgue produtos, serviços, cursos ou quaisquer materiais sem consultar os admins (em pvt);Se autorizado, ainda assim, a divulgação deste tipo de oferta deve ter link com o tema do grupo;Evite fazer flood com a divulgação de produtos e serviços;Se preferir, existem canais no telegram específicos para este tipo de atividade.''')

# Quando entra novo membro no grupo
@bot.message_handler(func=lambda m: True, content_types=['new_chat_member'])
def on_user_joins(m):
	print("Usuário \"@"+m.new_chat_member.username+"("+str(m.new_chat_member.id)+")\" entrou no grupo \""+m.chat.title+"("+str(m.chat.id)+")\".")
	arquivo.write("Usuário \"@"+m.new_chat_member.username+"("+str(m.new_chat_member.id)+")\" entrou no grupo \""+m.chat.title+"("+str(m.chat.id)+")\".\n")
	bot.send_message(m.chat.id, "Olá " + m.new_chat_member.first_name + ", bem vindo(a) ao grupo. Leia o post fixado e respeite os membros.")

# Gerar log de mensagens enviadas para conversa onde o bot esteja
@bot.message_handler(func=lambda m: True, content_types=['text'])
def gerarlog(m):
	arquivo.write(log_msg(m))

# Verificar se o chat é privado ou não
def verificarChat(m):
	if m == None:
		return(" Privado")
	else:
		return(": "+m)

bot.polling()
print(barra)
arquivo.write(barra)
arquivo.close()
