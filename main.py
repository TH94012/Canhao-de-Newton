import pygame, math as m
from pygame import *

class Projetil:
    def __init__(self, posicao, massa, velocidade, aceleracao, cor, raio):
        self.Posicao=list(posicao)
        self.Massa=massa
        self.Velocidade=list(velocidade)
        self.Aceleracao=list(aceleracao)
        self.Cor=cor
        self.Raio=raio
        self.Cos_t = None
        self.Sin_t = None
        self.Theta = None

    def atualizar(self):
        # tan = co/ca = y/x
        pos_x_rel = (self.Posicao[0]) - (largura/2)
        pos_y_rel = (self.Posicao[1]) - (altura/2)
        dist = distancia_entre_pontos(self.Posicao[0], self.Posicao[1],largura/2, altura/2)
        prod_m = massa_terra*self.Massa
        prod_dist = dist**2
        f_grav = G*prod_m/prod_dist
        cos = (largura/2-self.Posicao[0])/dist
        sen = (altura/2-self.Posicao[1])/dist
        self.Aceleracao[0] = f_grav*cos
        self.Aceleracao[1] = f_grav*sen
        '''#calculando o ângulo baseado no quandrante e no arctan
        tan = None
        try:
            tan = m.atan(pos_y_rel/ pos_x_rel)
        except ZeroDivisionError:
            tan = 0
        if pos_x_rel >= 0 and pos_y_rel >= 0 :
            self.Theta = tan
        elif pos_x_rel < 0 and pos_y_rel >= 0:
            self.Theta = tan + m.pi
        elif pos_x_rel < 0 and pos_y_rel < 0:
            self.Theta = tan + m.pi
        else:
            self.Theta = tan + 2*m.pi
        hip = m.sqrt((self.Posicao[0] - largura/2)**2 + (self.Posicao[1] - altura/2)**2)
        sin_t = -m.sin(self.Theta)
        cos_t = m.cos(self.Theta)
        self.Cos_t = pos_x_rel / hip
        self.Sin_t = pos_y_rel / hip
        self.Aceleracao[0] = G * massa_terra * cos_t/ hip**2
        self.Aceleracao[1] = G * massa_terra * sin_t/ hip**2'''
        """if self.Posicao[0] > largura/2:
            self.Aceleracao[0] = G * massa_terra/((self.Posicao[0]-190 - largura/2)**2)
        else:
            self.Aceleracao[0] = G * massa_terra/(-(self.Posicao[0]-190 - largura/2)**2)
        if self.Posicao[1] > altura/2:
            self.Aceleracao[1] = G * massa_terra/((self.Posicao[1] - altura/2)**2)
        else:
            self.Aceleracao[1] = G * massa_terra/(-(self.Posicao[1] - altura/2)**2)"""
        print(f"""({self.Aceleracao[0]}, {self.Aceleracao[1]})""")
        self.Velocidade[0] += self.Aceleracao[0]
        self.Velocidade[1] += self.Aceleracao[1]
        self.Posicao[0] += self.Velocidade[0]
        self.Posicao[1] += self.Velocidade[1]


def distancia_entre_pontos(x1, y1, x2, y2):
    return m.sqrt((x1-x2)**2 + (y1-y2)**2)

pygame.init()

G = 6.674184 * 10 ** (-11)
massa_terra = 20000000000000
massa_projetil = 1


largura, altura = 5472/5, 3648/5
tela = pygame.display.set_mode((largura, altura))
imagem_espaco = pygame.transform.scale(pygame.image.load(r"C:\Users\User\dev\Projeto Canhao de Newton\imagens\espaço2.jpg"), (largura, altura))
imagem_torre = pygame.transform.scale(pygame.image.load(r"C:\Users\User\dev\Projeto Canhao de Newton\imagens\torre.png"), (50, 50))
imagem_canhao = pygame.transform.scale(pygame.image.load(r"C:\Users\User\dev\Projeto Canhao de Newton\imagens\canhao.png"), (30, 30))
centro = (largura/2,altura/2)
fonte = pygame.font.SysFont("Arial", 30, True, True)


pygame.display.set_caption('Canhão de Newton')

projetil = Projetil((largura/2, altura/2-190), 1, (3, 0), (0, 0), (255, 255, 255), 5)

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

    projetil.atualizar()

    tela.blit(imagem_espaco, (0, 0))

    pygame.draw.circle(tela, (0, 0, 200), centro, 150)

    pygame.draw.circle(tela, projetil.Cor, projetil.Posicao, projetil.Raio)

    tela.blit(pygame.transform.rotate(imagem_canhao, -25), ((largura/2 - imagem_canhao.get_width()/2), altura/2 - imagem_canhao.get_height()/2- 200))
    tela.blit(imagem_torre, ((largura/2 - imagem_torre.get_width()/2), altura/2 - imagem_torre.get_height()/2- 170))

    mensagem_pos = F'Posição ({(projetil.Posicao[0] - largura/2):.2f}, {(projetil.Posicao[1] - altura/2):.2f})'
    mensagem_vel = F'Velocidade ({projetil.Velocidade[0]:.2f}, {projetil.Velocidade[1]:.2f})'
    mensagem_ace = F'Aceleração ({projetil.Aceleracao[0]:.2f}, {projetil.Aceleracao[1]:.2f})'

    tela.blit(fonte.render(mensagem_pos, False, (255, 255, 255)), (10, 30))
    tela.blit(fonte.render(mensagem_vel, False, (255, 255, 255)), (10, 60))
    tela.blit(fonte.render(mensagem_ace, False, (255, 255, 255)), (10, 90))

    pygame.display.flip()
    pygame.time.Clock().tick(60)