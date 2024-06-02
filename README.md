Entendi, aqui está o README ajustado com as instruções corretas para iniciar o servidor e o cliente:

---

# Slide Motion

Slide Motion é um projeto que permite controlar apresentações de slides usando apenas as mãos, com a ajuda de inteligência artificial e uma câmera. Com gestos simples, você pode avançar ou retroceder os slides de forma intuitiva e natural.

## Funcionalidades

- Controle de slides utilizando gestos manuais.
- Avance o slide tocando o dedo indicador no dedão da mão direita.
- Retroceda o slide tocando o dedo indicador no dedão da mão esquerda.
- Sistema dividido em servidor e cliente para maior flexibilidade e escalabilidade.

## Tecnologias Utilizadas

- **Inteligência Artificial (IA)**: Para reconhecimento de gestos das mãos utilizando a biblioteca `cvzone`.
- **Câmera**: Para capturar os movimentos das mãos.
- **Servidor**: Processa os gestos capturados e comunica com o cliente.
- **Cliente**: Interface para exibir e controlar os slides.

## Estrutura do Projeto

O projeto está dividido em duas partes principais:

### Servidor

O servidor é responsável por:

- Processar as imagens e reconhecer os gestos com a ajuda da biblioteca `cvzone`.
- Enviar comandos para o cliente com base nos gestos reconhecidos.

### Cliente

O cliente é responsável por:
- Capturar os gestos das mãos utilizando a câmera.
- Receber comandos do servidor.
- Avançar ou retroceder os slides conforme os comandos recebidos.

## Requisitos

- Windows
- Python 3.12
- Bibliotecas necessárias (listadas em `requirements.txt`)

## Instalação

### Passo a Passo

1. Clone o repositório:

    ```bash
    git clone https://github.com/seu-usuario/slide-motion.git
    cd slide-motion
    ```

2. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

3. Inicie o servidor executando `hand_detection_service.py`:

    ```bash
    python hand_detection_service.py
    ```

4. Inicie o cliente executando `main.py`:

    ```bash
    python main.py
    ```

## Como Usar

1. Posicione a câmera de forma que suas mãos fiquem visíveis.
2. Para avançar os slides, toque o dedo indicador no dedão da mão direita.
3. Para retroceder os slides, toque o dedo indicador no dedão da mão esquerda.

## Contribuição

Sinta-se à vontade para contribuir com o projeto. Para isso:

1. Fork o repositório.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`).
4. Faça o push da branch (`git push origin feature/nova-feature`).
5. Crie um novo Pull Request.

Este README fornece uma visão clara e abrangente do projeto Slide Motion, facilitando a instalação e o uso no ambiente Windows com Python 3.12, destacando o uso da biblioteca `cvzone` para o reconhecimento de gestos, e instruções para iniciar o servidor e o cliente.
