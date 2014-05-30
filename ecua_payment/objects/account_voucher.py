import time
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class account_voucher(osv.osv):
    _inherit = 'account.voucher'
    _name = 'account.voucher'


    _columns = {
        'reference': fields.char('Ref #', size=64, readonly=True, states={'draft':[('readonly',False)]}, help="Is the number of document payment is file (eg footnote exit # 043)"),
        'name':fields.char('Memo', size=256, readonly=True, states={'draft':[('readonly',False)]}, help="Provides an explanation of the payment."),
        'luck': fields.boolean('Luck amount'),
        'responsible_id':fields.many2one('res.users', 'Responsible', change_default=1, help="responsible for payment (is the user who approves the payment)"),
        
                }
    _defaults = {  
        'luck': True,
        'responsible_id':lambda self, cr, uid, context: uid,
        }
         
    def proforma_voucher(self, cr, uid, ids, context=None):
        "Si luck es True para bloquear y manar la ecepcion caso contrario que no mande la ecepcion y "
        obj_voucher_self = self.browse(cr, uid, ids)
        obj_voucher_line = self.pool.get('account.voucher.line')
        for o in obj_voucher_self:
            if o.luck:
                for so_ids in obj_voucher_line.search(cr,uid,[('voucher_id','=',o.id)]):
                    line = obj_voucher_line.browse(cr, uid, so_ids)
                    "comparar para lanzar excepcion"
                    if line.amount > line.amount_unreconciled: 
                        raise osv.except_osv(_('Warning!'),
                                        _('"Its unusual in online payment" amount "be a value larger than the" Initial Balance ", usually used to cross cents mismatch, in which case check uncheck" Block amount "do not forget to reconcile against the revenue account your accountant available (Example 2 cents to send the account 430500 - OTHER INCOME) "'))
                    else:
                        return super(account_voucher, self).proforma_voucher(cr, uid, ids, context=None)                    
            else:
                return super(account_voucher, self).proforma_voucher(cr, uid, ids, context=None)

    def button_print_pay_voucher(self, cr, uid, ids, context=None):
        #self.print_document_type(cr, uid, ids, context=context)
        self.button_proforma_voucher(cr, uid, ids, context=context)

        return True;
                
account_voucher()