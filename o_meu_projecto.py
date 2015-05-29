#  - - - - - -= = = Modulos exteriores = = = - - - - - - - - - - #

from robot import * # Modulo de comunicacao com o robot
from testes_tai import *


# - - - - - - - - = = = FUNCOES AUXILIARES - - - - - - - - - - = = = #

# - - - - - -Funcoes logicas - - - - - -#

def e_natural(numero):
    return (isinstance(numero,int)) and (numero >=0)

def e_igual(x,y):
    return x==y

# - Funcao tranforma caminho em sequencia de direccoes - -#

def transformar_caminho(lista):
    L=[]
    for i in range(len(lista)):
        for e in range(len(lista)-1):
            if i ==e+1:
                if lista [i][0]==lista[e][0]+1:
                    L=L+['sul']
                if lista [i][0]==lista[e][0]-1:
                    L=L+['norte']
                if lista [i][1]==lista[e][1]+1:
                    L=L+['este']
                if lista [i][1]==lista[e][1]-1:
                    L=L+['oeste']
    return inverter_direccoes(L)

# - -Funcao inverte a sequencia de direccoes, permitindo recuar - #

def inverter_direccoes(lista):
    inv=[]
    for i in range(len(lista)):
        if este_p(lista[i]):
            inv=inv+['oeste']
        elif oeste_p(lista[i]):
            inv=inv+['este']
        elif sul_p(lista[i]):
            inv=inv+['norte']
        elif norte_p(lista[i]):
            inv=inv+['sul']
    novo=[]
    for i in range(len(inv)-1,-1,-1):
        novo=novo+[inv[i]]
    return novo

#----funcao que determina a existencia de becos----#

def becos(controlo,pos,canal):
    posnorte=pos.posicao_relativa(norte)
    possul=pos.posicao_relativa(sul)
    poseste=pos.posicao_relativa(este)
    posoeste=pos.posicao_relativa(oeste)
    
    objnorte= controlo.estado_mapa().mapa_objecto_em(posnorte)
    objsul= controlo.estado_mapa().mapa_objecto_em(possul)
    objeste= controlo.estado_mapa().mapa_objecto_em(poseste)
    objoeste= controlo.estado_mapa().mapa_objecto_em(posoeste)
    
    n=0
    l=[objnorte,objsul,objeste,objoeste]
    for i in range(len(l)):
        if (l[i] == (desconhecido or comida or premio or monstro)):
            n=n+1
    if n==0:
        return True
    
    else:
        return False

# - - - - - -Funcao que verifica a existencia de desconhecidos  - - - - - -#
def mapa_completo(mapa):
    n=0
    for i in range(len(mapa)):
        for e in range(len(mapa[i])):
            if mapa[i][e]==desconhecido:
                n=n+1
                if n>1:
                    return False
    if mapa[-1][-1]!=desconhecido:
        return False
    for i in range(len(mapa[-1])):
        if mapa[-1][i]!=parede:
            return False
    for e in range(len(mapa)):
        if mapa[e][-1]!=parede:
            return False
    return True
#existe a hipotese de existir pelo menos 1 desconhecido no canto inferior direito

#--funcao que desliga o robot--#
def desliga(canal,controlo):
    mapa=controlo.mapa.devolve_mapa_original()
    robot_desliga(canal)
    print('         #-#-#-# Mapa Explorado #-#-#-#           ')
    print(controlo.estado_mapa())
    return canal,controlo

#--funcao que altera o estado e poe o robot a andar no mapa--#
def anda(canal,controlo):
    robot_anda(canal)
    controlo=controlo.estado_robot_avanca()

#funcao que executa robot_sente ate encontrar um objecto#
def sente(canal,controlo,mapa,pos_frente):
    if robot_sente_espaco(canal):
        mapa=mapa.desenvolve_mapa_original(pos_frente,espaco)
        if robot_energia(canal)==1:
            anda(canal,controlo)
            return desliga(canal,controlo)
        anda(canal,controlo)
        return canal, controlo
    
    elif robot_sente_parede(canal):
        mapa=mapa.desenvolve_mapa_original(pos_frente,parede)
        if robot_energia(canal)==1:
            return desliga(canal,controlo)
        robot_vira_direita(canal)
        controlo=controlo.estado_poe_objectos(pos_frente,parede).estado_robot_vira_direita()
        return canal, controlo

    elif robot_sente_premio(canal):
        mapa=mapa.desenvolve_mapa_original(pos_frente,premio)
        robot_apanha(canal)
        if robot_energia(canal)==1:
            anda(canal,controlo)
            return desliga(canal,controlo)
        anda(canal,controlo)
        return canal,controlo

    elif robot_sente_monstro(canal):
        mapa=mapa.desenvolve_mapa_original(pos_frente,monstro)
        robot_dispara(canal)
        anda(canal,controlo)
        return canal,controlo
    else:
        mapa=mapa.desenvolve_mapa_original(pos_frente,comida)
        robot_apanha(canal)
        if robot_energia(canal)==1:
            anda(canal,controlo)
            return desliga(canal,controlo)
        anda(canal,controlo)
        return canal,controlo

# - - - - - - = = = Definicao de tipos = = = - - - - - - - - #

# - - - - - - - - - - - - Tipo objecto - - - - - - - - - - - - #

espaco='c'
comida='r'
premio='s'
monstro='o'
parede='x'
desconhecido='d'

def espaco_p(objecto):
    return objecto==espaco

def comida_p(objecto):
    return objecto==comida

def premio_p(objecto):
    return objecto==premio

def monstro_p(objecto):
    return objecto==monstro

def parede_p(objecto):
    return objecto==parede

def desconhecido_p(objecto):
    return objecto==desconhecido

# - - - - - - - - - - Tipo direccao - - - - - - - - - - - - - - #

norte='norte'
sul='sul'
oeste='oeste'
este='este'

def norte_p(direccao):
    return direccao == norte
def sul_p(direccao):
    return direccao == sul
def oeste_p(direccao):
    return direccao == oeste
def este_p(direccao):
    return direccao == este

def vira_esquerda(direccao):
    
    if norte_p(direccao):
        return oeste
    elif oeste_p(direccao):
        return sul
    elif sul_p(direccao):
        return este
    elif este_p(direccao):
        return norte

def vira_direita(direccao):
    
    if norte_p(direccao):
        return este
    elif este_p(direccao):
        return sul
    elif sul_p(direccao):
        return oeste
    elif oeste_p(direccao):
        return norte

# - - - - - - - - - - - - Tipo posicao - - - - - - - - - - - - #

class posicao:
    
    def __init__ (self,linha,coluna):
        if (e_natural(linha) and e_natural(coluna))==True :
            self.c=coluna
            self.l=linha
        else:
            raise TypeError('posicao: linha/coluna nao e um inteiro positivo')
    
    def posicao_linha(self):
        return self.l
    
    def posicao_coluna(self):
        return self.c
    
    def posicao_igual(self,pos):
        return e_igual(self.c,pos.posicao_coluna()) and e_igual(self.l,pos.posicao_linha())
    
    def posicao_relativa(self,direccao):
        if norte_p(direccao):
            return posicao(self.l-1,self.c)
        elif sul_p(direccao):
            return posicao(self.l+1,self.c)
        elif oeste_p(direccao):
            return posicao(self.l,self.c-1)
        elif este_p(direccao):
            return posicao(self.l,self.c+1)
        else:
            raise TypeError('posicao_relativa: direccao nao e valida')

# - - - - - - - - - - - - Tipo mapa, INCLUINDO ALGUMAS FUNCOES AUXILIARES  - - - - - - - - - - #

class mapa:
    
    def __init__(self):
        self.col = 3
        self.lin = 3
        self.cont=[[parede,parede,parede],[parede,espaco,desconhecido],[parede,desconhecido,desconhecido]]
        self.modifica=[[(0,0),'x']]
        self.original=[['x']]
    
    def __repr__(self):
        mapa=''
        monstros=0
        comidas=0
        premios=0
        espacos=0
        paredes=0
        n=self.lin
        self.original[-1][-1]=parede
        for linha in range(self.lin):
            if n==int((self.lin)/2):
                mapa=mapa+str(self.original[linha])+'|'+str(self.lin)+' '+'linhas'+ '\n'
            else:
                mapa=mapa+str(self.original[linha])+'|'+'\n'
            n=n-1
        mapa=mapa + (self.col*'_____')+ '\n' +str(self.col)+' '+'colunas'+'\n'
        l=[]
        for i in range(len(self.modifica)):
            if monstro_p(self.modifica[i][1]):
                monstros=monstros+1
            elif premio_p(self.modifica[i][1]):
                premios=premios+1
            elif comida_p(self.modifica[i][1]):
                comidas=comidas+1
            elif parede_p(self.modifica[i][1]):
                paredes=paredes+1
            elif espaco_p(self.modifica[i][1]):
                espacos=espacos+1
        
        mapa=mapa+'\n'+'#-#-#-#-#-# Estatisticas #-#-#-#-#-#'+'\n'+'\n'
        mapa=mapa+ 'Numero de passagens pelos monstros vistos:' +' '+str(monstros) + '\n'+'Numero de passagens pelas comidas vistos:' +' '+str(premios)+'\n'+'Numero de passagens pelos premios vistos:' +' '+str(comidas)+'\n' + 'Caminho percorrido' + ' '+str(espacos+comidas+premios+monstros)
        return mapa

def mapa_objecto_em(self,pos):
    linha=pos.posicao_linha()
    coluna=pos.posicao_coluna()
    if (linha <= self.lin-1) and (coluna<= self.col-1):
            return self.cont[linha][coluna]
    else:
        return desconhecido

def mapa_poe_objecto_em(self,pos,objecto):
    linha=pos.posicao_linha()
    coluna=pos.posicao_coluna()
    if linha+1 > self.lin or coluna +1> self.col:
            return self.novo_mapa(linha,coluna,objecto)
    self.cont[linha][coluna]=objecto
    return self

def mapa_altura(self):
    return self.lin
    
    def mapa_largura(self):
        return self.col
    
    def novo_mapa(self,linha,coluna,objecto):
        while len(self.cont) < linha + 1:
            self.cont=self.cont+[[parede,desconhecido]]
        for c in range(len(self.cont)):
            while len(self.cont[c]) < coluna+1 :
                self.cont[c]=self.cont[c]+[desconhecido]
        self.lin=len(self.cont)
        self.col=len(self.cont[0])
        for i in range(len(self.cont)):
            while len(self.cont[i]) < self.col:
                self.cont[i]=self.cont[i]+[desconhecido]
        for c in range(len(self.cont[0])):
            self.cont[0][c]=parede
        return self.mapa_poe_objecto_em(posicao(linha,coluna),objecto)

    def mostra_mapa(self):
        return self.cont

    def desenvolve_mapa_original(self,pos,obj):
        self.modifica=self.modifica+[[(pos.posicao_linha(),pos.posicao_coluna()),obj]]
        return self

    def devolve_mapa_original(self):
        lista=self.cont
        for p in range(len(self.modifica)):
            coluna=self.modifica[p][0][1]
            linha=self.modifica[p][0][0]
            objecto=self.modifica[p][1]
            lista[linha][coluna]=objecto
        self.original=lista
        return self

# - - - - - - - - - - Tipo caminho, INCLUINDO ALGUMAS FUNCOES AUXILIARES - - - - - - - - - - - - #

class caminho:
    
    def __init__(self,pos):
        if isinstance(pos,posicao):
            self.l=pos.posicao_linha()
            self.c=pos.posicao_coluna()
            self.cam=[(self.l,self.c)]
        else:
            raise TypeError('caminho: arg nao e uma posicao')

def caminho_junta_posicao(self,direcao):
    pos=posicao(self.l,self.c).posicao_relativa(direcao)
    self.l=pos.posicao_linha()
    self.c=pos.posicao_coluna()
    self.cam=self.cam+[(self.l,self.c)]
    return self
    
    def cria_caminho(self, antes_apos_elimina):
        if antes_apos_elimina=='apos':
            self.cam=self.cam[1:]
            return self
        
        elif antes_apos_elimina=='antes':
            self.cam=self.cam[:-1]
            return self
        
        elif antes_apos_elimina=='elimina':
            count=0
            for cam1 in range(len(self.cam)-1,-1,-1):
                for cam2 in range(len(self.cam)-1,-1,-1):
                    if posicao(self.cam[cam1][0],self.cam[cam1][1]).posicao_igual(posicao(self.cam[cam2][0],self.cam[cam2][1])) and cam1!=cam2:
                        if cam1<cam2:
                            count=count+1
                            del[self.cam[cam1:cam2]]
                            novo=self
                            return novo.caminho_elimina_ciclos()
            if count==0:
                return self

def caminho_origem(self):
    return posicao(self.cam[0][0],self.cam[0][1])
    
    def caminho_apos_origem(self):
        novo=self
        return novo.cria_caminho('apos')
    
    def caminho_destino(self):
        return posicao(self.cam[-1][0],self.cam[-1][1])
    
    def caminho_antes_destino(self):
        novo=self
        return novo.cria_caminho('antes')
    
    def caminho_comprimento(self):
        return len(self.cam)
    
    def caminho_contem_ciclo(self):
        for cam1 in range(len(self.cam)):
            for cam2 in range(len(self.cam)):
                if self.cam[cam1]==self.cam[cam2] and cam1!=cam2:
                    return True
        return False
    
    def caminho_elimina_ciclos(self):
        novo=self
        return novo.cria_caminho('elimina')
    
    def mostra_caminho(self):
        return self.cam

# - - - - - - - - - - Tipo estado, INCLUINDO ALGUMAS FUNCOES AUXILIARES - - - - - - - - - - #

class estado:
    
    def __init__(self,pos,dire):
        if norte_p(dire) or oeste_p(dire) or este_p(dire) or sul_p(dire):
            self.l=pos.posicao_linha()
            self.c=pos.posicao_coluna()
            self.d=dire
            self.objecto=espaco
            self.caminho=caminho(pos)
            self.mapa=mapa()
            self.pos_frente=posicao(self.l,self.c).posicao_relativa(self.d)
        else:
            raise ValueError('estado: arg direccao nao e valido')

def cria_estado(self):
    self.l=1
    self.c=1
    self.d=este
    self.caminho=caminho(posicao(1,1))
    self.mapa=mapa().mapa_poe_objecto_em(posicao(1,1),espaco)
    return self
    
    def estado_robot_avanca(self):
        pos=posicao(self.l,self.c)
        self.l=pos.posicao_relativa(self.d).posicao_linha()
        self.c=pos.posicao_relativa(self.d).posicao_coluna()
        
        self.mapa=self.mapa.mapa_poe_objecto_em(posicao(self.l,self.c),espaco)
        self.caminho=self.caminho.caminho_junta_posicao(self.d)
        return self
    
    def estado_robot_vira_direita(self):
        self.d=vira_direita(self.d)
        return self
    
    def estado_robot_vira_esquerda(self):
        self.d=vira_esquerda(self.d)
        return self
    
    def estado_robot_apanha(self):
        pos=posicao(self.l,self.c)
        self.l=pos.posicao_linha()
        self.c=pos.posicao_coluna()
        self.mapa=self.mapa.mapa_poe_objecto_em(posicao(self.l,self.c),espaco)
        return self
    
    def estado_robot_dispara(self):
        pos=posicao(self.l,self.c)
        self.l=pos.posicao_linha()
        self.c=pos.posicao_coluna()
        self.mapa=self.mapa.mapa_poe_objecto_em(posicao(self.l,self.c),espaco)
        return self
    
    def estado_posicao_robot(self):
        return posicao(self.l,self.c)
    
    def estado_direccao_robot(self):
        return self.d
    
    def estado_mapa(self):
        return self.mapa
    
    def estado_caminho_percorrido(self):
        return self.caminho
    
    def estado_poe_objectos(self,pos,obj):
        self.mapa=self.mapa.mapa_poe_objecto_em(pos,obj)
        return self

# = = = Controlo do Robot = = = #

def controla_robot(canal,controlo):
    
    #-----Debug-----#
    time.sleep(1/30)
    
    # = Atribuicoes feitas em termos de posicao,direcao,mapa,caminho,posicao a frente,posicao a esquerda, e um caminho com objectos = #
    pos=controlo.estado_posicao_robot()
    dire=controlo.estado_direccao_robot()
    mapa=controlo.estado_mapa()
    cam=controlo.estado_caminho_percorrido()
    pos_frente=pos.posicao_relativa(dire)
    posi=pos.posicao_relativa(vira_esquerda(dire))
    posd=pos.posicao_relativa(vira_direita(dire))
    
    # = = = = = Definicoes de decisoes a tomar = = = = = #
    if mapa_completo(mapa.mostra_mapa()):
        return desliga(canal,controlo)
    elif robot_energia(canal)==1:
        return desliga(canal,controlo)
    else:
        #Verifica se a posicao onde se encontra e um beco ou nao#
        if becos(controlo,pos,canal):
            cami=cam.mostra_caminho()
            l=transformar_caminho(cami)
            #Se for beco ele vai tomar o caminho inverso ate encontrar um desconhecido#
            if robot_energia(canal)<3:
                return desliga(canal,controlo)
            else:
                if l!=[]:
                    if este_p(l[0]):
                        if norte_p(dire):
                            controlo=controlo.estado_robot_vira_direita().estado_robot_avanca()
                            robot_vira_direita(canal)
                            robot_anda(canal)
                        elif sul_p(dire):
                            controlo=controlo.estado_robot_vira_esquerda().estado_robot_avanca()
                            robot_vira_esquerda(canal)
                            robot_anda(canal)
                        elif oeste_p(dire):
                            controlo=controlo.estado_robot_vira_direita().estado_robot_vira_direita().estado_robot_avanca()
                            robot_vira_direita(canal)
                            robot_vira_direita(canal)
                            robot_anda(canal)
                        elif este_p(dire):
                            controlo=controlo.estado_robot_avanca()
                            robot_anda(canal)
                    elif sul_p(l[0]):
                        if este_p(dire):
                            controlo=controlo.estado_robot_vira_direita().estado_robot_avanca()
                            robot_vira_direita(canal)
                            robot_anda(canal)
                        elif oeste_p(dire):
                            controlo=controlo.estado_robot_vira_esquerda().estado_robot_avanca()
                            robot_vira_esquerda(canal)
                            robot_anda(canal)
                        elif norte_p(dire):
                            controlo=controlo.estado_robot_vira_direita().estado_robot_vira_direita().estado_robot_avanca()
                            robot_vira_direita(canal)
                            robot_vira_direita(canal)
                            robot_anda(canal)
                        elif sul_p(dire):
                            controlo=controlo.estado_robot_avanca()
                            robot_anda(canal)
                    elif norte_p(l[0]):
                        if oeste_p(dire):
                            controlo=controlo.estado_robot_vira_direita().estado_robot_avanca()
                            robot_vira_direita(canal)
                            robot_anda(canal)
                        elif este_p(dire):
                            controlo=controlo.estado_robot_vira_esquerda().estado_robot_avanca()
                            robot_vira_esquerda(canal)
                            robot_anda(canal)
                        elif sul_p(dire):
                            controlo=controlo.estado_robot_vira_direita().estado_robot_vira_direita().estado_robot_avanca()
                            robot_vira_direita(canal)
                            robot_vira_direita(canal)
                            robot_anda(canal)
                        elif norte_p(dire):
                            controlo=controlo.estado_robot_avanca()
                            robot_anda(canal)
                    elif oeste_p(l[0]):
                        if sul_p(dire):
                            controlo=controlo.estado_robot_vira_direita().estado_robot_avanca()
                            robot_vira_direita(canal)
                            robot_anda(canal)
                        elif norte_p(dire):
                            controlo=controlo.estado_robot_vira_esquerda().estado_robot_avanca()
                            robot_vira_esquerda(canal)
                            robot_anda(canal)
                        elif este_p(dire):
                            controlo=controlo.estado_robot_vira_direita().estado_robot_vira_direita().estado_robot_avanca()
                            robot_vira_direita(canal)
                            robot_vira_direita(canal)
                            robot_anda(canal)
                        elif oeste_p(dire):
                            controlo=controlo.estado_robot_avanca()
                            robot_anda(canal)
                    if robot_energia(canal)<=1:
                        return desliga(canal,controlo)
                    else:
                        cam=cam.caminho_elimina_ciclos()# no final elimina os ciclos para quando voltar para tras nao repetir direcoes inversas
                        return canal,controlo

                # se esta hipotese existir, significa que o robot percorreu o mapa todo e desliga se #
                else:
                    return desliga(canal,controlo)
        else:
            # = = = Se nao for beco verificase as posicoes a esquerda no mapa de navegacao = = = = = = = #
            if (parede_p(mapa.mapa_objecto_em(posi)) or espaco_p(mapa.mapa_objecto_em(posi))):
                # = = = Verifica se a posicao em frente e desconhecido no mapa de navegacao = = = = = = = #
                if desconhecido_p(mapa.mapa_objecto_em(pos_frente)):
                    return sente(canal,controlo,mapa,pos_frente)
                elif desconhecido_p(mapa.mapa_objecto_em(posi)):
                    robot_vira_esquerda(canal)
                    controlo=controlo.estado_robot_vira_esquerda()
                    return sente(canal,controlo,mapa,pos.posicao_relativa(dire))
                
                # = = = Caso seja desconhecido tera que evocar a funcao robot_sente = = = = = = = #
                # Ao mesmo tempo que ele usa as funcoes robot, o programa actualiza o estado #
                else:
                    robot_vira_direita(canal)
                    controlo=controlo.estado_robot_vira_direita()
                    return canal,controlo
            else:
                robot_vira_esquerda(canal)
                controlo=controlo.estado_robot_vira_esquerda()
                return canal,controlo