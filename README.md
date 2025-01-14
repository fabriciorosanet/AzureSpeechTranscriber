
![image](https://github.com/user-attachments/assets/6f03abe5-bced-4b7e-b75a-0d2ea46522c1) ![image](https://github.com/user-attachments/assets/93f2e1c9-7d3d-4ce6-ae52-a39d71c1fee2)



# Transcrição de Áudio e Identificação de Palavras-chave

Este projeto realiza a extração de áudio de um vídeo, transcreve o áudio usando o serviço de reconhecimento de fala da Azure, e identifica momentos específicos em que certas palavras-chave aparecem na transcrição.


## Funcionalidades

- **Extração de áudio**: Converte um arquivo de vídeo em um arquivo de áudio com configurações específicas para transcrição.
- **Transcrição**: Utiliza a API de reconhecimento de fala da Azure para transcrever o áudio extraído em português.
- **Identificação de palavras-chave**: Localiza momentos específicos da transcrição onde palavras-chave são mencionadas e calcula um timestamp aproximado.
- **Salvamento da transcrição**: Salva a transcrição completa e os momentos das palavras-chave em um arquivo de texto para consulta futura.

## Requisitos

- Python 3.x
- Bibliotecas Python:
  - `azure-cognitiveservices-speech`
  - `moviepy`
  - `tkinter `
- Conta no Azure com a API de reconhecimento de fala habilitada. Você precisará de uma chave de assinatura e da região do serviço.

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio


2. Instale as bibliotecas necessárias utilizando o `pip`:

   ```bash
   pip install azure-cognitiveservices-speech moviepy

3. Substitua a chave de assinatura e a região do serviço na função transcrever_azure no código com suas informações da conta Azure.

## Como usar

1. Defina o caminho do arquivo de vídeo (video_file_path) que você deseja processar.
2. Especifique o caminho onde deseja salvar o áudio extraído (audio_file_path) e o arquivo de transcrição (output_txt_path).
3. Configure as palavras-chave que você deseja identificar na transcrição.
4. Execute o script.
    ```bash
        python main.py

## Interface gráfica
1. Selecione o arquivo de vídeo que deseja processar.
2. Clique no botão "Process Video" para iniciar o processo de extração, transcrição e identificação das palavras-chave.
3. Configure as palavras-chave que você deseja identificar diretamente no código (na lista palavras_chave dentro da função process_video).

## Execução
Ao executar o script, você verá a transcrição completa do áudio e os momentos das palavras-chave identificadas no console, além de um arquivo de texto contendo essas informações.

## Arquivo de saída
A transcrição e os momentos das palavras-chave são salvos em um arquivo .txt conforme o caminho especificado (output_txt_path), e o progresso da transcrição é mostrado em uma barra de progresso. (Ainda precisa de ajustes)


<h2 id="colab">🤝 Colaboradores</h2>

<table>
  <tr>
    <td align="center">
      <a href="#">
        <img src="https://media.licdn.com/dms/image/v2/D4D03AQFhg6aT98EYyQ/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1697061290400?e=1735171200&v=beta&t=I7QymWDGwsoAsobMDPcCba6KiP3cvSA8LnWUF2G9nzU" width="100px;" alt="Fabricio Rosa"/><br>
        <sub>
          <b>Fabrício Rosa</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#">
        <img src="https://media.licdn.com/dms/image/v2/D4D03AQE-5o3qpWIN9g/profile-displayphoto-shrink_100_100/profile-displayphoto-shrink_100_100/0/1710954940792?e=1735171200&v=beta&t=7vLCKrr7DJio8MREsd9pBijdp8TjUFA5RdkCJpetsS0" width="100px;" alt="Eduardo Bortoli"/><br>
        <sub>
          <b>Eduardo Bortoli</b>
        </sub>
      </a>
    </td>
