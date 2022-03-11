from odoo import fields, models

class PosConfig(models.Model):
    _inherit = 'pos.config'
    _description = 'Customer modification for PDV settings'

    vsao_POS_filter_Partner = fields.Boolean(string='Mostrar somente Clientes do PDV?')


    def get_limited_partners_loading(self):
        if not self.vsao_POS_filter_Partner:
            self.env.cr.execute("""
                WITH pm AS
                (
                        SELECT   partner_id,
                                Count(partner_id) order_count
                        FROM     pos_order
                        GROUP BY partner_id)
                SELECT    id
                FROM      res_partner AS partner
                LEFT JOIN pm
                ON        (
                                    partner.id = pm.partner_id)
                ORDER BY  COALESCE(pm.order_count, 0) DESC,
                        NAME limit %s;
            """, [str(self.limited_partners_amount)])
            result = self.env.cr.fetchall()
        else:
            self.env.cr.execute("""
                WITH pm AS
                (
                        SELECT   partner_id,
                                Count(partner_id) order_count
                        FROM     pos_order
                        GROUP BY partner_id)
                SELECT    id
                FROM      res_partner AS partner
                LEFT JOIN pm
                ON        (
                                    partner.id = pm.partner_id)
                WHERE "partner.vsao_POS_available" = 1
                ORDER BY  COALESCE(pm.order_count, 0) DESC,
                        NAME limit %s;
            """, [str(self.limited_partners_amount)])
            result = self.env.cr.fetchall()
        return result