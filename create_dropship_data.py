#!/usr/bin/env python3
"""
Script para criar dados de teste de Automatic Dropship via API EPCIS
Baseado na estrutura XML capturada da gravação de tela
"""
import requests
import uuid
from datetime import datetime, timedelta
import random
import string

# Configurações
BASE_URL = "https://qualityportal.qa-test.tracktraceweb.com"
API_URL = f"{BASE_URL}/api/epcis"

# Credenciais (mesmas do CLAUDE.md)
USERNAME = "teste@teste.com"
PASSWORD = "Mudar@12345344"


def generate_serial():
    """Gera um número serial único"""
    return ''.join(random.choices(string.digits, k=12))


def generate_gtin():
    """Gera um GTIN válido para teste"""
    # Usando GTIN base visto nos prints
    return "00897513000001"


def generate_lot():
    """Gera número de lote"""
    return f"LOT{random.randint(10000, 99999)}"


def generate_po_number():
    """Gera número de PO"""
    return f"PO{random.randint(100000, 999999)}"


def get_auth_token(session):
    """Faz login e obtém token de autenticação"""

    # Tentar diferentes endpoints de login
    login_endpoints = [
        f"{BASE_URL}/api/auth/login",
        f"{BASE_URL}/api/v1/auth/login",
        f"{BASE_URL}/auth/login",
        f"{BASE_URL}/api/login",
    ]

    payload = {
        "username": USERNAME,
        "password": PASSWORD
    }

    for login_url in login_endpoints:
        try:
            print(f"   Tentando: {login_url}")
            response = session.post(login_url, json=payload)
            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                try:
                    data = response.json()
                    token = data.get("token") or data.get("access_token") or data.get("jwt")
                    if token:
                        return token
                except:
                    pass
            elif response.status_code == 404:
                continue
            else:
                print(f"   Resposta: {response.text[:100] if response.text else 'vazio'}")
        except Exception as e:
            print(f"   Erro: {e}")

    return None


def create_epcis_xml(po_number, serial, gtin, lot):
    """Cria XML EPCIS para dropship baseado na estrutura capturada"""

    event_id = str(uuid.uuid4())
    event_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")

    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<epcis:EPCISDocument xmlns:epcis="urn:epcglobal:epcis:xsd:1"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    schemaVersion="1.2" creationDate="{event_time}">
    <EPCISBody>
        <EventList>
            <ObjectEvent>
                <eventTime>{event_time}</eventTime>
                <eventTimeZoneOffset>-03:00</eventTimeZoneOffset>
                <epcList>
                    <epc>urn:epc:id:sgtin:{gtin}.{serial}</epc>
                </epcList>
                <action>OBSERVE</action>
                <bizStep>urn:epcglobal:cbv:bizstep:shipping</bizStep>
                <disposition>urn:epcglobal:cbv:disp:in_transit</disposition>
                <readPoint>
                    <id>urn:epc:id:sgln:0897513.00001.0</id>
                </readPoint>
                <bizTransactionList>
                    <bizTransaction type="urn:epcglobal:cbv:btt:po">{po_number}</bizTransaction>
                </bizTransactionList>
                <extension>
                    <sourceList>
                        <source type="urn:epcglobal:cbv:sdt:owning_party">urn:epc:id:sgln:0897513.00001.0</source>
                    </sourceList>
                    <destinationList>
                        <destination type="urn:epcglobal:cbv:sdt:owning_party">urn:epc:id:sgln:0123456.00001.0</destination>
                    </destinationList>
                    <ilmd>
                        <lotNumber>{lot}</lotNumber>
                        <itemExpirationDate>2026-12-31</itemExpirationDate>
                    </ilmd>
                </extension>
            </ObjectEvent>
        </EventList>
    </EPCISBody>
</epcis:EPCISDocument>'''

    return xml


def send_epcis_event(session, xml_content, token=None):
    """Envia evento EPCIS para a API"""

    headers = {
        "Content-Type": "application/xml",
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    # Tentar diferentes endpoints
    endpoints = [
        f"{BASE_URL}/api/epcis/events",
        f"{BASE_URL}/api/epcis",
        f"{BASE_URL}/api/v1/epcis/events",
        f"{BASE_URL}/api/dropship/import",
    ]

    for endpoint in endpoints:
        try:
            print(f"Tentando endpoint: {endpoint}")
            response = session.post(endpoint, data=xml_content, headers=headers)
            print(f"  Status: {response.status_code}")

            if response.status_code in [200, 201, 202]:
                print(f"  Sucesso!")
                return True, response
            else:
                print(f"  Resposta: {response.text[:200] if response.text else 'vazio'}")
        except Exception as e:
            print(f"  Erro: {e}")

    return False, None


def main():
    print("=" * 60)
    print("CRIAÇÃO DE DADOS DE TESTE - AUTOMATIC DROPSHIP")
    print("=" * 60)

    session = requests.Session()

    # Login
    print("\n1. Fazendo login...")
    token = get_auth_token(session)

    if not token:
        print("   Tentando sem token...")
    else:
        print(f"   Token obtido: {token[:20]}...")

    # Criar dados
    print("\n2. Gerando dados de teste...")
    po_number = generate_po_number()
    serial = generate_serial()
    gtin = generate_gtin()
    lot = generate_lot()

    print(f"   PO Number: {po_number}")
    print(f"   Serial: {serial}")
    print(f"   GTIN: {gtin}")
    print(f"   Lot: {lot}")

    # Criar XML
    print("\n3. Criando XML EPCIS...")
    xml_content = create_epcis_xml(po_number, serial, gtin, lot)
    print(f"   XML criado ({len(xml_content)} bytes)")

    # Enviar
    print("\n4. Enviando para API...")
    success, response = send_epcis_event(session, xml_content, token)

    if success:
        print("\n✓ Dados criados com sucesso!")
        print(f"  PO Number para pesquisa: {po_number}")
    else:
        print("\n✗ Não foi possível criar via API")
        print("\nAlternativas:")
        print("1. Verificar se existe endpoint de importação de XML no portal")
        print("2. Criar dados manualmente via interface")
        print("3. Usar endpoint correto da API (consultar documentação)")

    # Salvar XML para uso manual
    xml_file = "/home/filipe/Área de trabalho/RPA/test_dropship.xml"
    with open(xml_file, "w") as f:
        f.write(xml_content)
    print(f"\nXML salvo em: {xml_file}")
    print("Você pode importar este arquivo manualmente se necessário.")


if __name__ == "__main__":
    main()
