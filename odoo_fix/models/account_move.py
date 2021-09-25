import re
from datetime import datetime
from random import SystemRandom

from odoo import api, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _validate_for_eletronic_document(self):
        errors = []
        for move in self:
            if not move.company_id.l10n_br_certificate:
                errors.append('Cadastro da Empresa - Certificado Digital')
            if not move.company_id.l10n_br_cert_password:
                errors.append('Cadastro da Empresa - Senha do Certificado Digital')
            if not move.company_id.partner_id.l10n_br_legal_name:
                errors.append('Cadastro da Empresa - Razão Social')
            if not move.company_id.partner_id.l10n_br_cnpj_cpf:
                errors.append('Cadastro da Empresa - CNPJ/CPF')
            if not move.company_id.partner_id.street:
                errors.append('Cadastro da Empresa / Endereço - Logradouro')
            if not move.company_id.partner_id.l10n_br_number:
                errors.append('Cadastro da Empresa / Endereço - Número')
            if not move.company_id.partner_id.zip or len(
                    re.sub(r"\D", "", self.company_id.partner_id.zip)) != 8:
                errors.append('Cadastro da Empresa / Endereço - CEP')
            if not move.company_id.partner_id.state_id:
                errors.append('Cadastro da Empresa / Endereço - Estado')
            else:
                if not move.company_id.partner_id.state_id.l10n_br_ibge_code:
                    errors.append('Cadastro da Empresa / Endereço - Cód. do IBGE do estado')
                if not move.company_id.partner_id.state_id.name:
                    errors.append('Cadastro da Empresa / Endereço - Nome do estado')

            if not move.company_id.partner_id.city_id:
                errors.append('Cadastro da Empresa / Endereço - município')
            else:
                if not move.company_id.partner_id.city_id.name:
                    errors.append('Cadastro da Empresa / Endereço - Nome do município')
                if not move.company_id.partner_id.city_id.l10n_br_ibge_code:
                    errors.append('Cadastro da Empresa/Endereço - Cód. do IBGE do município')

            if not move.company_id.partner_id.country_id:
                errors.append('Cadastro da Empresa / Endereço - país')
            else:
                if not move.company_id.partner_id.country_id.name:
                    errors.append('Cadastro da Empresa / Endereço - Nome do país')
                if not move.company_id.partner_id.country_id.l10n_br_ibge_code:
                    errors.append('Cadastro da Empresa / Endereço - Código do BC do país')

            responsavel_tecnico = move.company_id.l10n_br_responsavel_tecnico_id
            if responsavel_tecnico:
                if not responsavel_tecnico.l10n_br_cnpj_cpf:
                    errors.append("Configure o CNPJ do responsável técnico")
                if not responsavel_tecnico.email:
                    errors.append("Configure o Email do responsável técnico")
                if not responsavel_tecnico.phone:
                    errors.append("Configure o Telefone do responsável técnico")
                if len(responsavel_tecnico.child_ids) == 0:
                    errors.append("Adicione um contato para o responsável técnico!")

            has_products = has_services = False
            # produtos
            # Remove section, note, delivery, expense and insurance lines
            doc_lines = move.invoice_line_ids.filtered(
                lambda x: not (x.display_type or x.is_delivery_expense_or_insurance())
            )
            for eletr in doc_lines:
                if eletr.product_id.type == 'service':
                    has_services = True
                if eletr.product_id.type in ('consu', 'product'):
                    has_products = True
                prod = "Produto: %s - %s" % (eletr.product_id.default_code,
                                             eletr.product_id.name)
                if not eletr.product_id.default_code:
                    errors.append(
                        'Prod: %s - Código do produto' % (
                            eletr.product_id.name))
                # if has_products and not eletr.product_id.l10n_br_ncm_id: VSAO 25.09.2021: Change for not check Service with NCM when NF has both items
                if eletr.product_id.type in ('consu', 'product') and not eletr.product_id.l10n_br_ncm_id:
                    errors.append('%s - NCM do produto' % prod)

                if not move.fiscal_position_id:
                    errors.append('Configure a posição fiscal')
                if move.company_id.l10n_br_accountant_id and not \
                        move.company_id.l10n_br_accountant_id.l10n_br_cnpj_cpf:
                    errors.append('Cadastro da Empresa / CNPJ do escritório contabilidade')

            if has_products and not move.company_id.l10n_br_nfe_sequence:
                errors.append('Configure a sequência para numeração de NFe')
            if has_services and not move.company_id.l10n_br_nfe_service_sequence:
                errors.append('Configure a sequência para numeração de NFe de serviço')

            # Verificar os campos necessários para envio de nfse (serviço)
            if has_services:
                cod_municipio = '%s%s' % (
                    move.company_id.state_id.l10n_br_ibge_code,
                    move.company_id.city_id.l10n_br_ibge_code,
                )
                if cod_municipio == '4205407':
                    if not all([
                        move.company_id.l10n_br_aedf,
                        move.company_id.l10n_br_client_id,
                        move.company_id.l10n_br_client_secret,
                        move.company_id.l10n_br_user_password
                    ]):
                        errors.append('Campos de validação para a API de Florianópolis não estão preenchidos')
                elif cod_municipio in ['3550308', '3106200']:
                    for line in move.invoice_line_ids:
                        if line.product_id.type == 'service':
                            if not line.product_id.service_type_id:
                                errors.append('Produto %s não possui Tipo de Serviço.' % line.product_id.name)
                            if not line.product_id.service_code:
                                errors.append('Produto %s não possui Código do Município.' % line.product_id.name)
                else:
                    if not move.company_id.l10n_br_nfse_token_acess:
                        errors.append('Token da Focus não está preenchida!\nPor favor, preencha-a no cadastro da empresa.')

            partner = move.partner_id.commercial_partner_id
            company = move.company_id
            # Destinatário
            if partner.is_company and not partner.l10n_br_legal_name:
                errors.append('Cliente - Razão Social')

            if partner.country_id.id == company.partner_id.country_id.id:
                if not partner.l10n_br_cnpj_cpf:
                    errors.append('Cliente - CNPJ/CPF')

            if not partner.street:
                errors.append('Cliente / Endereço - Logradouro')

            if not partner.l10n_br_number:
                errors.append('Cliente / Endereço - Número')

            if partner.country_id.id == company.partner_id.country_id.id:
                if not partner.zip or len(
                        re.sub(r"\D", "", partner.zip)) != 8:
                    errors.append('Cliente / Endereço - CEP')

            if partner.country_id.id == company.partner_id.country_id.id:
                if not partner.state_id:
                    errors.append('Cliente / Endereço - Estado')
                else:
                    if not partner.state_id.l10n_br_ibge_code:
                        errors.append('Cliente / Endereço - Código do IBGE \
                                    do estado')
                    if not partner.state_id.name:
                        errors.append('Cliente / Endereço - Nome do estado')

            if partner.country_id.id == company.partner_id.country_id.id:
                if not partner.city_id:
                    errors.append('Cliente / Endereço - Município')
                else:
                    if not partner.city_id.name:
                        errors.append('Cliente / Endereço - Nome do \
                                    município')
                    if not partner.city_id.l10n_br_ibge_code:
                        errors.append('Cliente / Endereço - Código do IBGE \
                                    do município')

            if not partner.country_id:
                errors.append('Cliente / Endereço - País')
            else:
                if not partner.country_id.name:
                    errors.append('Cliente / Endereço - Nome do país')
                if not partner.country_id.l10n_br_ibge_code:
                    errors.append('Cliente / Endereço - Cód. do BC do país')

        if len(errors) > 0:
            msg = "\n".join(
                ["Por favor corrija os erros antes de prosseguir"] + errors)
            raise UserError(msg)
