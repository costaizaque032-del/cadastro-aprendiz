# ==================================================
# SITE: CADASTRO JOVEM APRENDIZ
# Acessa pelo navegador, de qualquer celular/computador
# ==================================================
import streamlit as st
from PIL import Image, ImageDraw
from datetime import datetime
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

st.set_page_config(page_title="Cadastro Jovem Aprendiz", layout="wide")
st.title("📋 CADASTRO — JOVEM APRENDIZ")

# ------------------- FUNÇÃO SALVAR ASSINATURA -------------------
def assinatura_para_imagem(dados_assinatura, tamanho=(300, 120)):
    img = Image.new("RGB", tamanho, "white")
    desenho = ImageDraw.Draw(img)
    if dados_assinatura:
        for i in range(len(dados_assinatura) - 1):
            x1, y1 = dados_assinatura[i]
            x2, y2 = dados_assinatura[i+1]
            desenho.line([(x1, y1), (x2, y2)], fill="black", width=2)
    return img

# ------------------- FORMULÁRIO -------------------
st.header("📋 Dados do Jovem Aprendiz")
col1, col2 = st.columns(2)
with col1:
    nome = st.text_input("Nome Completo")
    nascimento = st.text_input("Data de Nascimento")
    cpf = st.text_input("CPF")
    rg = st.text_input("RG / Órgão Emissor")
    endereco = st.text_input("Endereço Completo")
    bairro = st.text_input("Bairro")
with col2:
    cidade = st.text_input("Cidade / UF")
    cep = st.text_input("CEP")
    telefone = st.text_input("Telefone")
    email = st.text_input("E-mail")
    escola = st.text_input("Escola que estuda")
    serie = st.text_input("Série/Ano")

st.header("👤 Dados do Responsável Legal")
col1, col2 = st.columns(2)
with col1:
    resp_nome = st.text_input("Nome Completo do Responsável")
    resp_cpf = st.text_input("CPF do Responsável")
    resp_rg = st.text_input("RG do Responsável")
with col2:
    resp_parentesco = st.text_input("Grau de Parentesco")
    resp_telefone = st.text_input("Telefone do Responsável")
    resp_email = st.text_input("E-mail do Responsável")

st.header("📎 Anexar Documentos")
arquivos = st.file_uploader("Selecione RG, comprovante, etc.", 
                             accept_multiple_files=True,
                             type=["pdf", "jpg", "jpeg", "png"])

st.header("✍️ Assinaturas")
st.info("💡 Desenhe a assinatura com o mouse/dedo na área abaixo")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Assinatura do Aprendiz")
    ass_aprendiz = st.text_area("Desenhe aqui (clique e escreva)", height=120, 
                                placeholder="Escreva seu nome com o mouse...")
with col2:
    st.subheader("Assinatura do Responsável")
    ass_resp = st.text_area("Desenhe aqui", height=120, 
                           placeholder="Escreva seu nome com o mouse...")

# ------------------- GERAR PDF -------------------
def gerar_pdf():
    if not nome:
        st.error("❌ Preencha o Nome Completo!")
        return None
    
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    largura, altura = A4
    margem = 50

    # Cabeçalho
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(largura/2, altura - 60, "FICHA DE CADASTRO — JOVEM APRENDIZ")
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(largura/2, altura - 80, 
                         f"Data de Emissão: {datetime.now().strftime('%d/%m/%Y às %H:%M')}")
    pdf.line(margem, altura - 90, largura - margem, altura - 90)

    y = altura - 110

    def escrever(rotulo, valor):
        nonlocal y
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(margem, y, rotulo + ":")
        pdf.setFont("Helvetica", 11)
        pdf.drawString(margem + 150, y, valor if valor else "—")
        y -= 25

    # Dados Aprendiz
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(margem, y, "📋 DADOS DO APRENDIZ")
    y -= 20
    escrever("Nome Completo", nome)
    escrever("Nascimento", nascimento)
    escrever("CPF", cpf)
    escrever("RG", rg)
    escrever("Endereço", endereco)
    escrever("Bairro", bairro)
    escrever("Cidade/UF", cidade)
    escrever("CEP", cep)
    escrever("Telefone", telefone)
    escrever("E-mail", email)
    escrever("Escola", escola)
    escrever("Série/Ano", serie)

    y -= 10
    pdf.line(margem, y, largura - margem, y)
    y -= 20

    # Dados Responsável
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(margem, y, "👤 DADOS DO RESPONSÁVEL LEGAL")
    y -= 20
    escrever("Nome Completo", resp_nome)
    escrever("CPF", resp_cpf)
    escrever("RG", resp_rg)
    escrever("Parentesco", resp_parentesco)
    escrever("Telefone", resp_telefone)
    escrever("E-mail", resp_email)

    y -= 10
    pdf.line(margem, y, largura - margem, y)
    y -= 20

    # Documentos
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(margem, y, "📎 DOCUMENTOS ANEXADOS")
    y -= 20
    if arquivos:
        for doc in arquivos:
            pdf.setFont("Helvetica", 10)
            pdf.drawString(margem + 10, y, f"• {doc.name}")
            y -= 18
    else:
        pdf.setFont("Helvetica", 10)
        pdf.drawString(margem + 10, y, "Nenhum documento anexado")
        y -= 18

    y -= 30

    # Assinaturas
    pdf.drawString(margem, y, "Assinatura do Jovem Aprendiz:")
    y -= 40
    pdf.drawString(margem, y, ass_aprendiz[:100])
    y -= 20
    pdf.drawString(margem, y, "_________________________________________")
    pdf.drawString(margem, y-15, nome)

    y -= 40
    pdf.drawString(largura/2 + 30, y + 40, "Assinatura do Responsável Legal:")
    y -= 40
    pdf.drawString(largura/2 + 30, y, ass_resp[:100])
    y -= 20
    pdf.drawString(largura/2 + 30, y, "_________________________________________")
    pdf.drawString(largura/2 + 30, y-15, resp_nome)

    pdf.save()
    buffer.seek(0)
    return buffer

# Botão final
if st.button("✅ GERAR CADASTRO FINAL", type="primary"):
    pdf = gerar_pdf()
    if pdf:
        st.success("🎉 Cadastro gerado com sucesso!")
        st.download_button(
            label="📥 Baixar PDF",
            data=pdf,
            file_name=f"cadastro_{nome.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )
        st.balloons()