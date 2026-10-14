# Analyzers Experts — Laboratório Virtual de Cromatografia Gasosa

Protótipo educacional em Streamlit para explorar cromatogramas simulados, tempos de retenção, largura de pico e resolução aproximada.

## Executar localmente

1. Instale Python 3.10 ou superior.
2. Abra um terminal na pasta deste projeto.
3. (Recomendado) crie um ambiente virtual:

   Windows:
   ```powershell
   py -m venv .venv
   .venv\Scripts\activate
   ```

   macOS/Linux:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

5. Execute:

   ```bash
   streamlit run app.py
   ```

O Streamlit abrirá a aplicação no navegador.

## Publicar online

Uma opção simples para prototipagem é publicar o repositório no GitHub e conectá-lo a um serviço de hospedagem compatível com Streamlit. Para incorporar ao AnalyzersExperts.com, hospede a aplicação e incorpore-a por iframe se a hospedagem e as políticas do site permitirem. Para conteúdo pago, implemente autenticação e autorização no servidor; não confie apenas em esconder links ou botões.

## Limitações científicas

Este é um modelo didático com picos gaussianos e relações simplificadas entre parâmetros. Não é um simulador validado de um instrumento comercial, não modela termodinâmica de retenção real e não deve ser usado para decisões de processo. A retenção não é determinada apenas pela massa molecular.
