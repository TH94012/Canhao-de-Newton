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
        dist = distancia_entre_pontos(self.Posicao[0], self.Posicao[1],largura/2, altura/2)
        prod_m = massa_terra*self.Massa
        prod_dist = dist**2
        f_grav = G*prod_m/prod_dist
        cos = (largura/2-self.Posicao[0])/dist
        sen = (altura/2-self.Posicao[1])/dist
        self.Aceleracao[0] = f_grav*cos
        self.Aceleracao[1] = f_grav*sen
        self.Velocidade[0] += self.Aceleracao[0]
        self.Velocidade[1] += self.Aceleracao[1]
        self.Posicao[0] += self.Velocidade[0]
        self.Posicao[1] += self.Velocidade[1]


def distancia_entre_pontos(x1, y1, x2, y2):
    return m.sqrt((x1-x2)**2 + (y1-y2)**2)

pygame.init()

largura, altura = 5472/5, 3648/5
G = 6.674184 * 10 ** (-11)
massa_terra = 20000000000000
massa_projetil = 1
perielio = [None, None]
afelio = [None, None]
x_rel = 0
y_rel = 0
k_w = k_s = k_a = k_d = None
seguir_proj = False

tela = pygame.display.set_mode((largura, altura))
imagem_mais = pygame.image.load(R'imagens\mais.png')
imagem_espaco = pygame.transform.scale(pygame.image.load(r"imagens\espaço2.jpg"), (largura, altura))
imagem_torre = pygame.transform.scale(pygame.image.load(r"imagens\torre.png"), (50, 50))
imagem_canhao = pygame.transform.scale(pygame.image.load(r"imagens\canhao.png"), (30, 30))
imagem_terra = pygame.image.load(R'imagens\terraDia copy.png')
fonte = pygame.font.SysFont("Arial", 30, True, True)


pygame.display.set_caption('Canhão de Newton')

projetil = Projetil((largura/2, altura/2-195), 1, (3, 0), (0, 0), (255, 255, 255), 5)
perielio = [projetil.Posicao[0], projetil.Posicao[1]]

primeira = True

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_w:
                k_w = True
            if evento.key == pygame.K_s:
                k_s = True
            if evento.key == pygame.K_a:
                k_a = True
            if evento.key == pygame.K_d:
                k_d = True
            if evento.key == pygame.K_e:
                seguir_proj = not seguir_proj
                if not seguir_proj:
                    x_rel = y_rel = 0
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_w:
                k_w = False
            if evento.key == pygame.K_s:
                k_s = False
            if evento.key == pygame.K_a:
                k_a = False
            if evento.key == pygame.K_d:
                k_d = False
        
    if k_w:
        y_rel -= 2
    if k_s:
        y_rel += 2
    if k_a:
        x_rel -= 2
    if k_d:
        x_rel += 2

    projetil.atualizar()

    if seguir_proj:
        x_rel = projetil.Posicao[0] - largura/2
        y_rel = projetil.Posicao[1] - altura/2

    if primeira:
        afelio[0] = perielio[0] = projetil.Posicao[0]
        afelio[1] = perielio[1] = projetil.Posicao[1]


    if distancia_entre_pontos(projetil.Posicao[0], projetil.Posicao[1], largura/2, altura/2) > distancia_entre_pontos(afelio[0], afelio[1], largura/2, altura/2):
        afelio = (projetil.Posicao[0], projetil.Posicao[1])

    if distancia_entre_pontos(projetil.Posicao[0], projetil.Posicao[1], largura/2, altura/2) < distancia_entre_pontos(perielio[0], perielio[1], largura/2, altura/2):
        perielio = (projetil.Posicao[0], projetil.Posicao[1])


    tela.blit(imagem_espaco, (0, 0))

    tela.blit(imagem_terra, (largura/2 - imagem_terra.get_width()/2 - x_rel, altura/2 - imagem_terra.get_height()/2 - y_rel))
    tela.blit(imagem_mais, (largura/2 - imagem_mais.get_width()/2 - x_rel, altura/2 - imagem_mais.get_height()/2 - y_rel))

    pygame.draw.circle(tela, projetil.Cor, (projetil.Posicao[0] - x_rel, projetil.Posicao[1] - y_rel), projetil.Raio)

    tela.blit(pygame.transform.rotate(imagem_canhao, -25), (largura/2 - imagem_canhao.get_width()/2 - x_rel, altura/2 - imagem_canhao.get_height()/2- 200 - y_rel))
    tela.blit(imagem_torre, (largura/2 - imagem_torre.get_width()/2 - x_rel, altura/2 - imagem_torre.get_height()/2- 170 - y_rel))

    #desenhar perielio
    pygame.draw.circle(tela, (0, 255, 0), (perielio[0] - x_rel, perielio[1] - y_rel), projetil.Raio)
    
    #desenhar afelio
    pygame.draw.circle(tela, (255, 0, 0), (afelio[0] - x_rel, afelio[1] - y_rel), projetil.Raio)

    mensagem_pos = F'Posição ({(projetil.Posicao[0] - largura/2):.2f}, {(projetil.Posicao[1] - altura/2):.2f})'
    mensagem_vel = F'Velocidade ({projetil.Velocidade[0]:.2f}, {projetil.Velocidade[1]:.2f})'
    mensagem_ace = F'Aceleração ({projetil.Aceleracao[0]:.2f}, {projetil.Aceleracao[1]:.2f})'

    tela.blit(fonte.render(mensagem_pos, False, (255, 255, 255)), (10, 30))
    tela.blit(fonte.render(mensagem_vel, False, (255, 255, 255)), (10, 60))
    tela.blit(fonte.render(mensagem_ace, False, (255, 255, 255)), (10, 90))

    primeira = False
    pygame.display.flip()
    pygame.time.Clock().tick(120)